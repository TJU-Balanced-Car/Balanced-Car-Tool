# -*- coding: utf-8 -*-

import sys
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5 import QtWidgets, QtCore
from mainWindow import Ui_MainWindow

def list_serial_ports():
    """获取串口列表"""
    ports = serial.tools.list_ports.comports()
    return [(port.device, port.description) for port in ports]

class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.populate_ports()  # 填充 Port 下拉菜单

    def populate_ports(self):
        ports = list_serial_ports()
        self.Port.clear()  # 清空现有选项
        # 添加带描述的端口选项，例如 "COM3 - Arduino Uno"
        for port, description in ports:
            self.Port.addItem(f"{port} - {description}", port)

def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()
