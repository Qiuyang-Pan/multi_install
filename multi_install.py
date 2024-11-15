# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'multi_install.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(766, 480)
        Form.setAcceptDrops(True)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setObjectName("verticalLayout")
        self.label = QtWidgets.QLabel(Form)
        self.label.setObjectName("label")
        self.verticalLayout.addWidget(self.label)
        self.tableView = QtWidgets.QTableView(Form)
        self.tableView.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableView.setAutoFillBackground(True)
        self.tableView.setEditTriggers(QtWidgets.QAbstractItemView.NoEditTriggers)
        self.tableView.setDefaultDropAction(QtCore.Qt.IgnoreAction)
        self.tableView.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
        self.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.tableView.setTextElideMode(QtCore.Qt.ElideMiddle)
        self.tableView.setObjectName("tableView")
        self.tableView.horizontalHeader().setDefaultSectionSize(203)
        self.tableView.horizontalHeader().setMinimumSectionSize(100)
        self.tableView.horizontalHeader().setStretchLastSection(False)
        self.tableView.verticalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.tableView)
        self.selectApk = QtWidgets.QWidget(Form)
        self.selectApk.setEnabled(True)
        self.selectApk.setMinimumSize(QtCore.QSize(0, 23))
        self.selectApk.setMaximumSize(QtCore.QSize(16777215, 23))
        self.selectApk.setAutoFillBackground(False)
        self.selectApk.setObjectName("selectApk")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.selectApk)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.filePath = QtWidgets.QPlainTextEdit(self.selectApk)
        self.filePath.setEnabled(True)
        self.filePath.setMaximumSize(QtCore.QSize(16777215, 23))
        self.filePath.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.filePath.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.filePath.setSizeAdjustPolicy(QtWidgets.QAbstractScrollArea.AdjustIgnored)
        self.filePath.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.filePath.setReadOnly(True)
        self.filePath.setPlaceholderText("请选择要安装的APK文件，可拖拽APK到窗口获取路径！")
        self.filePath.setObjectName("filePath")
        self.horizontalLayout_4.addWidget(self.filePath)
        self.openFileBtn = QtWidgets.QPushButton(self.selectApk)
        self.openFileBtn.setMaximumSize(QtCore.QSize(86, 23))
        self.openFileBtn.setObjectName("openFileBtn")
        self.horizontalLayout_4.addWidget(self.openFileBtn)
        self.verticalLayout.addWidget(self.selectApk)
        self.action = QtWidgets.QWidget(Form)
        self.action.setMaximumSize(QtCore.QSize(16777215, 180))
        self.action.setObjectName("action")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.action)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.widget = QtWidgets.QWidget(self.action)
        self.widget.setObjectName("widget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.widget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.showDevicesBtn = QtWidgets.QPushButton(self.widget)
        self.showDevicesBtn.setObjectName("showDevicesBtn")
        self.verticalLayout_2.addWidget(self.showDevicesBtn)
        self.installSelectBtn = QtWidgets.QPushButton(self.widget)
        self.installSelectBtn.setObjectName("installSelectBtn")
        self.verticalLayout_2.addWidget(self.installSelectBtn)
        self.installAllBtn = QtWidgets.QPushButton(self.widget)
        self.installAllBtn.setObjectName("installAllBtn")
        self.verticalLayout_2.addWidget(self.installAllBtn)
        self.horizontalLayout_5.addWidget(self.widget)
        self.output = QtWidgets.QPlainTextEdit(self.action)
        self.output.setMaximumSize(QtCore.QSize(16777215, 180))
        self.output.setReadOnly(True)
        self.output.setObjectName("output")
        self.horizontalLayout_5.addWidget(self.output)
        self.verticalLayout.addWidget(self.action)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "multi_install"))
        self.label.setText(_translate("Form", "使用前需先在本地安装adb！！！"))
        self.openFileBtn.setText(_translate("Form", "选择安装的apk"))
        self.showDevicesBtn.setText(_translate("Form", "刷新设备"))
        self.installSelectBtn.setText(_translate("Form", "安装到选中设备"))
        self.installAllBtn.setText(_translate("Form", "安装到所有设备"))
