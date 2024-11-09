# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainWindow.ui'
#
# Created by: PyQt5 UI code generator 5.15.11
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 553)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setMaximumSize(QtCore.QSize(16777215, 100))
        self.frame.setStyleSheet("QFrame \n"
"{\n"
"    background-color: rgb(255, 255, 255)\n"
"}")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.layoutWidget = QtWidgets.QWidget(self.frame)
        self.layoutWidget.setGeometry(QtCore.QRect(41, 19, 341, 64))
        self.layoutWidget.setObjectName("layoutWidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.layoutWidget)
        self.gridLayout_2.setContentsMargins(0, 0, 0, 0)
        self.gridLayout_2.setHorizontalSpacing(98)
        self.gridLayout_2.setVerticalSpacing(16)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setContentsMargins(0, -1, -1, -1)
        self.horizontalLayout_3.setSpacing(20)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.Bytesize = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        self.Bytesize.setFont(font)
        self.Bytesize.setObjectName("Bytesize")
        self.Bytesize.addItem("")
        self.Bytesize.addItem("")
        self.Bytesize.addItem("")
        self.Bytesize.addItem("")
        self.horizontalLayout_3.addWidget(self.Bytesize)
        self.gridLayout_2.addLayout(self.horizontalLayout_3, 0, 1, 1, 1)
        self.horizontalLayout_9 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(20)
        self.horizontalLayout_9.setObjectName("horizontalLayout_9")
        self.label_9 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        self.label_9.setFont(font)
        self.label_9.setObjectName("label_9")
        self.horizontalLayout_9.addWidget(self.label_9)
        self.Parity = QtWidgets.QComboBox(self.layoutWidget)
        self.Parity.setMinimumSize(QtCore.QSize(63, 0))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(8)
        self.Parity.setFont(font)
        self.Parity.setObjectName("Parity")
        self.Parity.addItem("")
        self.Parity.addItem("")
        self.Parity.addItem("")
        self.horizontalLayout_9.addWidget(self.Parity)
        self.gridLayout_2.addLayout(self.horizontalLayout_9, 1, 0, 1, 1)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setSpacing(20)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.Baudrate = QtWidgets.QComboBox(self.layoutWidget)
        self.Baudrate.setMinimumSize(QtCore.QSize(63, 0))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        self.Baudrate.setFont(font)
        self.Baudrate.setObjectName("Baudrate")
        self.Baudrate.addItem("")
        self.Baudrate.addItem("")
        self.Baudrate.addItem("")
        self.Baudrate.addItem("")
        self.horizontalLayout_2.addWidget(self.Baudrate)
        self.gridLayout_2.addLayout(self.horizontalLayout_2, 0, 0, 1, 1)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setSpacing(20)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_4 = QtWidgets.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_4.addWidget(self.label_4)
        self.Stopbits = QtWidgets.QComboBox(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        self.Stopbits.setFont(font)
        self.Stopbits.setObjectName("Stopbits")
        self.Stopbits.addItem("")
        self.Stopbits.addItem("")
        self.Stopbits.addItem("")
        self.horizontalLayout_4.addWidget(self.Stopbits)
        self.gridLayout_2.addLayout(self.horizontalLayout_4, 1, 1, 1, 1)
        self.layoutWidget1 = QtWidgets.QWidget(self.frame)
        self.layoutWidget1.setGeometry(QtCore.QRect(480, 20, 266, 23))
        self.layoutWidget1.setObjectName("layoutWidget1")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(20)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.Port = QtWidgets.QComboBox(self.layoutWidget1)
        self.Port.setMinimumSize(QtCore.QSize(199, 0))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        self.Port.setFont(font)
        self.Port.setObjectName("Port")
        self.horizontalLayout.addWidget(self.Port)
        self.layoutWidget2 = QtWidgets.QWidget(self.frame)
        self.layoutWidget2.setGeometry(QtCore.QRect(490, 60, 251, 32))
        self.layoutWidget2.setObjectName("layoutWidget2")
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(self.layoutWidget2)
        self.horizontalLayout_5.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_5.setSpacing(70)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.BLEBtn = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.BLEBtn.setFont(font)
        self.BLEBtn.setObjectName("BLEBtn")
        self.horizontalLayout_5.addWidget(self.BLEBtn)
        self.SerialBtn = QtWidgets.QPushButton(self.layoutWidget2)
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.SerialBtn.setFont(font)
        self.SerialBtn.setObjectName("SerialBtn")
        self.horizontalLayout_5.addWidget(self.SerialBtn)
        self.gridLayout.addWidget(self.frame, 0, 0, 1, 2)
        self.frame_Data = QtWidgets.QFrame(self.centralwidget)
        self.frame_Data.setMaximumSize(QtCore.QSize(300, 16777215))
        self.frame_Data.setStyleSheet("QFrame {\n"
"    background-color: rgb(229, 229, 229)\n"
"}")
        self.frame_Data.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_Data.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_Data.setObjectName("frame_Data")
        self.layoutWidget3 = QtWidgets.QWidget(self.frame_Data)
        self.layoutWidget3.setGeometry(QtCore.QRect(40, 270, 208, 144))
        self.layoutWidget3.setObjectName("layoutWidget3")
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(self.layoutWidget3)
        self.verticalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_4.setSpacing(7)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.label_10 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_10.setMinimumSize(QtCore.QSize(112, 0))
        self.label_10.setMaximumSize(QtCore.QSize(112, 16777215))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(14)
        self.label_10.setFont(font)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_10.addWidget(self.label_10)
        self.Roll = QtWidgets.QLabel(self.layoutWidget3)
        self.Roll.setMinimumSize(QtCore.QSize(86, 0))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(14)
        self.Roll.setFont(font)
        self.Roll.setObjectName("Roll")
        self.horizontalLayout_10.addWidget(self.Roll)
        self.verticalLayout_4.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_17 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_17.setObjectName("horizontalLayout_17")
        self.label_24 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_24.setMinimumSize(QtCore.QSize(112, 0))
        self.label_24.setMaximumSize(QtCore.QSize(112, 16777215))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(14)
        self.label_24.setFont(font)
        self.label_24.setObjectName("label_24")
        self.horizontalLayout_17.addWidget(self.label_24)
        self.label_25 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_25.setMinimumSize(QtCore.QSize(86, 0))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(14)
        self.label_25.setFont(font)
        self.label_25.setObjectName("label_25")
        self.horizontalLayout_17.addWidget(self.label_25)
        self.verticalLayout_4.addLayout(self.horizontalLayout_17)
        self.horizontalLayout_20 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_20.setObjectName("horizontalLayout_20")
        self.label_30 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_30.setMinimumSize(QtCore.QSize(112, 0))
        self.label_30.setMaximumSize(QtCore.QSize(112, 16777215))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(14)
        self.label_30.setFont(font)
        self.label_30.setObjectName("label_30")
        self.horizontalLayout_20.addWidget(self.label_30)
        self.label_31 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_31.setMinimumSize(QtCore.QSize(86, 0))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(14)
        self.label_31.setFont(font)
        self.label_31.setObjectName("label_31")
        self.horizontalLayout_20.addWidget(self.label_31)
        self.verticalLayout_4.addLayout(self.horizontalLayout_20)
        self.horizontalLayout_21 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_21.setObjectName("horizontalLayout_21")
        self.label_32 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_32.setMinimumSize(QtCore.QSize(112, 0))
        self.label_32.setMaximumSize(QtCore.QSize(112, 16777215))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(14)
        self.label_32.setFont(font)
        self.label_32.setObjectName("label_32")
        self.horizontalLayout_21.addWidget(self.label_32)
        self.label_33 = QtWidgets.QLabel(self.layoutWidget3)
        self.label_33.setMinimumSize(QtCore.QSize(86, 0))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(14)
        self.label_33.setFont(font)
        self.label_33.setObjectName("label_33")
        self.horizontalLayout_21.addWidget(self.label_33)
        self.verticalLayout_4.addLayout(self.horizontalLayout_21)
        self.ModelView = QtWidgets.QGraphicsView(self.frame_Data)
        self.ModelView.setGeometry(QtCore.QRect(30, 40, 241, 201))
        self.ModelView.setStyleSheet("QGraphicsView {\n"
"    border: none;\n"
"}")
        self.ModelView.setObjectName("ModelView")
        self.gridLayout.addWidget(self.frame_Data, 1, 0, 1, 1)
        self.frame_img = QtWidgets.QFrame(self.centralwidget)
        self.frame_img.setStyleSheet("QFrame \n"
"{\n"
"    background-color: rgb(255, 255, 255)\n"
"}")
        self.frame_img.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_img.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_img.setObjectName("frame_img")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.frame_img)
        self.gridLayout_3.setContentsMargins(19, 10, 22, 0)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.groupBox = QtWidgets.QGroupBox(self.frame_img)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.groupBox.setFont(font)
        self.groupBox.setObjectName("groupBox")
        self.layoutWidget4 = QtWidgets.QWidget(self.groupBox)
        self.layoutWidget4.setGeometry(QtCore.QRect(100, 30, 169, 140))
        self.layoutWidget4.setObjectName("layoutWidget4")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.layoutWidget4)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(14)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_11 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_11.setObjectName("horizontalLayout_11")
        self.label_12 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_12.setMinimumSize(QtCore.QSize(36, 0))
        self.label_12.setMaximumSize(QtCore.QSize(36, 16777215))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.label_12.setFont(font)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_11.addWidget(self.label_12)
        self.label_13 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_13.setMinimumSize(QtCore.QSize(122, 0))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.label_13.setFont(font)
        self.label_13.setObjectName("label_13")
        self.horizontalLayout_11.addWidget(self.label_13)
        self.verticalLayout_2.addLayout(self.horizontalLayout_11)
        self.horizontalLayout_12 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_12.setObjectName("horizontalLayout_12")
        self.label_14 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_14.setMinimumSize(QtCore.QSize(36, 0))
        self.label_14.setMaximumSize(QtCore.QSize(36, 16777215))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.label_14.setFont(font)
        self.label_14.setObjectName("label_14")
        self.horizontalLayout_12.addWidget(self.label_14)
        self.label_15 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_15.setMinimumSize(QtCore.QSize(122, 0))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.label_15.setFont(font)
        self.label_15.setObjectName("label_15")
        self.horizontalLayout_12.addWidget(self.label_15)
        self.verticalLayout_2.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_13 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_13.setObjectName("horizontalLayout_13")
        self.label_16 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_16.setMinimumSize(QtCore.QSize(36, 0))
        self.label_16.setMaximumSize(QtCore.QSize(36, 16777215))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.label_16.setFont(font)
        self.label_16.setObjectName("label_16")
        self.horizontalLayout_13.addWidget(self.label_16)
        self.label_17 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_17.setMinimumSize(QtCore.QSize(122, 0))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.label_17.setFont(font)
        self.label_17.setObjectName("label_17")
        self.horizontalLayout_13.addWidget(self.label_17)
        self.verticalLayout_2.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_18 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_18.setObjectName("horizontalLayout_18")
        self.label_26 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_26.setMinimumSize(QtCore.QSize(36, 0))
        self.label_26.setMaximumSize(QtCore.QSize(36, 16777215))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.label_26.setFont(font)
        self.label_26.setObjectName("label_26")
        self.horizontalLayout_18.addWidget(self.label_26)
        self.label_27 = QtWidgets.QLabel(self.layoutWidget4)
        self.label_27.setMinimumSize(QtCore.QSize(122, 0))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.label_27.setFont(font)
        self.label_27.setObjectName("label_27")
        self.horizontalLayout_18.addWidget(self.label_27)
        self.verticalLayout_2.addLayout(self.horizontalLayout_18)
        self.gridLayout_3.addWidget(self.groupBox, 0, 0, 1, 1)
        self.frame_2 = QtWidgets.QFrame(self.frame_img)
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 20))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.ConnectStatus = QtWidgets.QPushButton(self.frame_2)
        self.ConnectStatus.setGeometry(QtCore.QRect(364, 0, 91, 20))
        self.ConnectStatus.setStyleSheet("QPushButton {\n"
"    background-color: white;\n"
"    border: none;\n"
"}\n"
"QPushButton::hover{\n"
"    background-color: rgb(231, 231, 231);\n"
"}")
        self.ConnectStatus.setText("")
        self.ConnectStatus.setObjectName("ConnectStatus")
        self.gridLayout_3.addWidget(self.frame_2, 2, 0, 1, 1)
        self.groupBox_2 = QtWidgets.QGroupBox(self.frame_img)
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(16)
        self.groupBox_2.setFont(font)
        self.groupBox_2.setObjectName("groupBox_2")
        self.layoutWidget5 = QtWidgets.QWidget(self.groupBox_2)
        self.layoutWidget5.setGeometry(QtCore.QRect(100, 40, 168, 112))
        self.layoutWidget5.setObjectName("layoutWidget5")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.layoutWidget5)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setSpacing(19)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_14 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_14.setObjectName("horizontalLayout_14")
        self.label_18 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_18.setMinimumSize(QtCore.QSize(36, 0))
        self.label_18.setMaximumSize(QtCore.QSize(36, 16777215))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.label_18.setFont(font)
        self.label_18.setObjectName("label_18")
        self.horizontalLayout_14.addWidget(self.label_18)
        self.label_19 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_19.setMinimumSize(QtCore.QSize(122, 0))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.label_19.setFont(font)
        self.label_19.setObjectName("label_19")
        self.horizontalLayout_14.addWidget(self.label_19)
        self.verticalLayout_3.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_15 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_15.setObjectName("horizontalLayout_15")
        self.label_20 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_20.setMinimumSize(QtCore.QSize(36, 0))
        self.label_20.setMaximumSize(QtCore.QSize(36, 16777215))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.label_20.setFont(font)
        self.label_20.setObjectName("label_20")
        self.horizontalLayout_15.addWidget(self.label_20)
        self.label_21 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_21.setMinimumSize(QtCore.QSize(122, 0))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.label_21.setFont(font)
        self.label_21.setObjectName("label_21")
        self.horizontalLayout_15.addWidget(self.label_21)
        self.verticalLayout_3.addLayout(self.horizontalLayout_15)
        self.horizontalLayout_19 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_19.setObjectName("horizontalLayout_19")
        self.label_28 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_28.setMinimumSize(QtCore.QSize(36, 0))
        self.label_28.setMaximumSize(QtCore.QSize(36, 16777215))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.label_28.setFont(font)
        self.label_28.setObjectName("label_28")
        self.horizontalLayout_19.addWidget(self.label_28)
        self.label_29 = QtWidgets.QLabel(self.layoutWidget5)
        self.label_29.setMinimumSize(QtCore.QSize(122, 0))
        font = QtGui.QFont()
        font.setFamily("小米兰亭")
        font.setPointSize(12)
        self.label_29.setFont(font)
        self.label_29.setObjectName("label_29")
        self.horizontalLayout_19.addWidget(self.label_29)
        self.verticalLayout_3.addLayout(self.horizontalLayout_19)
        self.gridLayout_3.addWidget(self.groupBox_2, 1, 0, 1, 1)
        self.gridLayout.addWidget(self.frame_img, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 22))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.label_3.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">数据位</span></p></body></html>"))
        self.Bytesize.setItemText(0, _translate("MainWindow", "5"))
        self.Bytesize.setItemText(1, _translate("MainWindow", "6"))
        self.Bytesize.setItemText(2, _translate("MainWindow", "7"))
        self.Bytesize.setItemText(3, _translate("MainWindow", "8"))
        self.label_9.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">校验位</span></p></body></html>"))
        self.Parity.setItemText(0, _translate("MainWindow", "无"))
        self.Parity.setItemText(1, _translate("MainWindow", "奇校验"))
        self.Parity.setItemText(2, _translate("MainWindow", "偶校验"))
        self.label_2.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">波特率</span></p></body></html>"))
        self.Baudrate.setItemText(0, _translate("MainWindow", "4800"))
        self.Baudrate.setItemText(1, _translate("MainWindow", "9600"))
        self.Baudrate.setItemText(2, _translate("MainWindow", "38400"))
        self.Baudrate.setItemText(3, _translate("MainWindow", "115200"))
        self.label_4.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">停止位</span></p></body></html>"))
        self.Stopbits.setItemText(0, _translate("MainWindow", "1"))
        self.Stopbits.setItemText(1, _translate("MainWindow", "1.5"))
        self.Stopbits.setItemText(2, _translate("MainWindow", "2"))
        self.label.setText(_translate("MainWindow", "<html><head/><body><p><span style=\" font-size:11pt;\">端口号</span></p></body></html>"))
        self.BLEBtn.setText(_translate("MainWindow", "打开蓝牙串口"))
        self.SerialBtn.setText(_translate("MainWindow", "打开串口"))
        self.label_10.setText(_translate("MainWindow", "车体角度："))
        self.Roll.setText(_translate("MainWindow", "0"))
        self.label_24.setText(_translate("MainWindow", "动量轮转速："))
        self.label_25.setText(_translate("MainWindow", "0"))
        self.label_30.setText(_translate("MainWindow", "后轮转速："))
        self.label_31.setText(_translate("MainWindow", "0"))
        self.label_32.setText(_translate("MainWindow", "舵机角度："))
        self.label_33.setText(_translate("MainWindow", "0"))
        self.groupBox.setTitle(_translate("MainWindow", "直立环"))
        self.label_12.setText(_translate("MainWindow", "Kp："))
        self.label_13.setText(_translate("MainWindow", "0"))
        self.label_14.setText(_translate("MainWindow", "Ki："))
        self.label_15.setText(_translate("MainWindow", "0"))
        self.label_16.setText(_translate("MainWindow", "Kd："))
        self.label_17.setText(_translate("MainWindow", "0"))
        self.label_26.setText(_translate("MainWindow", "Out："))
        self.label_27.setText(_translate("MainWindow", "0"))
        self.groupBox_2.setTitle(_translate("MainWindow", "速度环"))
        self.label_18.setText(_translate("MainWindow", "Kp："))
        self.label_19.setText(_translate("MainWindow", "0"))
        self.label_20.setText(_translate("MainWindow", "Kd："))
        self.label_21.setText(_translate("MainWindow", "0"))
        self.label_28.setText(_translate("MainWindow", "Out："))
        self.label_29.setText(_translate("MainWindow", "0"))
