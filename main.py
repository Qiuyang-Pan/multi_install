import concurrent
import subprocess
import sys
import threading

from PyQt5.QtCore import Qt, QThread, pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QApplication, QMessageBox, QWidget, QFileDialog
from multi_install import *
from concurrent.futures import ThreadPoolExecutor


class MultiInstall(QWidget, Ui_Form):
    def __init__(self):
        super().__init__()
        self.install_thread = None
        self.setupUi(self)
        self.init_table()
        self.showDevicesBtn.clicked.connect(self.show_devices)
        self.installSelectBtn.clicked.connect(self.select_install)
        self.installAllBtn.clicked.connect(self.all_install)
        self.openFileBtn.clicked.connect(self.open_file_dialog)
        self.show()

        self.apk = ''
        self.devices_info = {}

    def open_file_dialog(self):
        options = QFileDialog.Options()
        fileName, _ = QFileDialog.getOpenFileName(self, "选择文件", "", "All Files (*);;Text Files (*.txt)",
                                                  options=options)
        if fileName:
            self.filePath.setPlainText(fileName)
            self.apk = fileName

    def init_table(self):
        self.model = QStandardItemModel()
        self.model.setHorizontalHeaderLabels(["device_id", "device_name"])
        self.tableView.setModel(self.model)

    def show_devices(self):
        self.init_table()
        # self.output.clear()
        self.get_devices_info()
        if self.devices_info:
            self.add_devices_to_table()

    def add_devices_to_table(self):
        for device_id, device_name in self.devices_info.items():
            print(device_id, device_name)
            # 添加到模型中
            id_model = QStandardItem(device_id)
            id_model.setTextAlignment(Qt.AlignCenter)
            name_model = QStandardItem(device_name)
            name_model.setTextAlignment(Qt.AlignCenter)
            self.model.appendRow([id_model, name_model])

    def get_devices_info(self):
        # 清空设备信息
        self.devices_info = {}
        # 执行 adb devices -l 命令
        result = subprocess.Popen(
            ['adb', 'devices', '-l'],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            creationflags=subprocess.CREATE_NO_WINDOW
        )
        stdout, stderr = result.communicate()
        # 检查是否有错误输出
        if stderr:
            print("Error:", stderr)
            QMessageBox.warning(self, "警告", "获取设备信息失败！")
            return None
        else:
            # 解析输出
            lines = stdout.splitlines()
            # 跳过第一行（标题行）
            for line in lines[1:]:
                if line:  # 非空行
                    parts = line.split()
                    device_id = parts[0]
                    model = None
                    for prop in parts[1:]:
                        if prop.startswith('model:'):
                            model = prop.split(':')[1]
                            break
                    if model:
                        self.devices_info[device_id] = model
            self.output.appendPlainText("获取设备信息成功！共获取到 {} 台设备！".format(len(self.devices_info)))

    def check_apk_and_devices(self, devices_info=None):
        """
        检查是否选择了APK文件和设备
        """
        if not devices_info:
            QMessageBox.warning(self, "警告", "没有可安装设备！请选择设备安装！")
            return
        if not self.apk:
            QMessageBox.warning(self, "警告", "请先选择APK文件！")
            self.open_file_dialog()
            return
        self.output.clear()
        self.output.appendPlainText("APK文件路径：{}".format(self.apk))
        return True

    def selected_devices(self):
        # 获取选择的设备id
        selected_indices = self.tableView.selectionModel().selectedRows()  # 获取选中的行索引
        if not selected_indices:
            return
        selected_devices = {}
        for index in selected_indices:
            # 获取设备ID，角色使用Qt.DisplayRole
            device_id = self.model.data(self.model.index(index.row(), 0), Qt.DisplayRole)
            device_name = self.model.data(self.model.index(index.row(), 1), Qt.DisplayRole)
            selected_devices[device_id] = device_name
        return selected_devices

    def select_install(self):
        select_devices = self.selected_devices()
        if self.check_apk_and_devices(select_devices):
            self.start_install_thread(select_devices)
            return
        if not self.devices_info:
            self.show_devices()

    def all_install(self):
        self.show_devices()
        if self.check_apk_and_devices(self.devices_info):
            self.start_install_thread(self.devices_info)

    def start_install_thread(self, devices_info):
        if devices_info:
            self.output.appendPlainText("正在获取安装设备，请稍等...")
            self.install_thread = InstallThread(devices_info, self.apk)
            self.install_thread.update_text.connect(self.update_plaintext)
            self.install_thread.start()

    def update_plaintext(self, text):
        self.output.appendPlainText(text)


class InstallThread(QThread):
    update_text = pyqtSignal(str)

    def __init__(self, devices_info, apk, parent=None):
        super(InstallThread, self).__init__(parent)
        self.device_info = devices_info
        self.apk = apk

    def run(self):
        with ThreadPoolExecutor(max_workers=len(self.device_info)) as executor:
            # 创建一个未来到设备名字的映射
            future_to_device_name = {executor.submit(self.install_apk, device_id, device_name, self.apk): device_name
                                     for
                                     device_id, device_name in self.device_info.items()}

            for future in concurrent.futures.as_completed(future_to_device_name):
                device_name = future_to_device_name[future]
                try:
                    result = future.result()
                    if result['success']:
                        output = f"{device_name} 安装完成:\n{result['stdout']}"
                    else:
                        output = f"{device_name} 安装失败:\n{result['stderr']}"
                except Exception as exc:
                    output = f"An error occurred on {device_name}: {exc}"
                self.update_text.emit("\n" + output)
        self.update_text.emit("所有设备安装完成。\n")

    def install_apk(self, device_id, device_name, apk_path):
        try:
            print(f"Thread {threading.current_thread().name} started installing on {device_name}")
            self.update_text.emit(f"{device_name} 开始安装")
            # 使用Popen代替run，并设置creationflags=CREATE_NO_WINDOW
            process = subprocess.Popen(
                ['adb', '-s', device_id, 'install', apk_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                creationflags=subprocess.CREATE_NO_WINDOW
            )
            # 等待进程完成
            stdout, stderr = process.communicate()
            return {'success': process.returncode == 0, 'stdout': stdout, 'stderr': stderr}
        except Exception as e:
            return {'success': False, 'stderr': str(e)}


if __name__ == '__main__':
    app = QApplication(sys.argv)
    multi_install = MultiInstall()
    sys.exit(app.exec_())
