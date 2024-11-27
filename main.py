# -*- coding: utf-8 -*-
# Author: Jacob Hu

import sys
import re
import asyncio
import serial
import serial.tools.list_ports
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QDialog, QWidget
from PyQt5.QtCore import Qt, QThread, QTimer
from PyQt5 import QtWidgets, QtCore
from mainWindow import Ui_MainWindow
from BLEWindow import Ui_Form as Ui_BLEWindow
from PyQt5.QtSvg import QGraphicsSvgItem
from bleak import BleakScanner, BleakClient
from bleak.backends.characteristic import BleakGATTCharacteristic

SRC_PATH = Path.absolute(Path(__file__)).parent  # Get temp path
icon_path = str(SRC_PATH / "img//model.svg")  # Add to get icon path
ser = serial.Serial()
class UnpackedData:
    def __init__(self):
        self.Roll = 0.0
        self.Motor1Speed = 0
        self.Motor2Speed = 0
        self.ServoAngle = 0
        self.velKp = 0.0
        self.velKi = 0.0
        self.velKd = 0.0
        self.velOut = 0.0
        self.angleKp = 0.0
        self.angleKi = 0.0
        self.angleKd = 0.0
        self.angleOut = 0.0
        self.accKp = 0.0
        self.accKi = 0.0
        self.accKd = 0.0
        self.accOut = 0.0

# 创建UnpackedData实例
unpacked_data = UnpackedData()
# 正则表达式匹配模式
pattern = {
    'Roll':         r'R:\s*([+-]?\d*\.\d+|\d+)',     # 匹配R:后面的float数字
    'Motor1Speed':  r'M1:\s*([+-]?\d+)',             # 匹配M1:后面的int数字
    'Motor2Speed':  r'M2:\s*([+-]?\d+)',             # 匹配M2:后面的int数字
    'ServoAngle':   r'S:\s*([+-]?\d+)',              # 匹配S:后面的int数字
    'velKp':        r'Vp:\s*([+-]?\d*\.\d+|\d+)',    # 匹配Vp:后的float数字
    'velKi':        r'Vi:\s*([+-]?\d*\.\d+|\d+)',    # 匹配Vi:后的float数字
    'velKd':        r'Vd:\s*([+-]?\d*\.\d+|\d+)',    # 匹配Vd:后的float数字
    'velOut':       r'Vo:\s*([+-]?\d*\.\d+|\d+)',    # 匹配Vo:后的float数字
    'angleKp':      r'Ap:\s*([+-]?\d*\.\d+|\d+)',    # 匹配Ap:后的float数字
    'angleKi':      r'Ai:\s*([+-]?\d*\.\d+|\d+)',    # 匹配Ai:后的float数字
    'angleKd':      r'Ad:\s*([+-]?\d*\.\d+|\d+)',    # 匹配Ad:后的float数字
    'angleOut':     r'Ao:\s*([+-]?\d*\.\d+|\d+)',    # 匹配Ao:后的float数字
    'accKp':        r'Cp:\s*([+-]?\d*\.\d+|\d+)',    # 匹配Cp:后的float数字
    'accKi':        r'Ci:\s*([+-]?\d*\.\d+|\d+)',    # 匹配Ci:后的float数字
    'accKd':        r'Cd:\s*([+-]?\d*\.\d+|\d+)',    # 匹配Cd:后的float数字
    'accOut':       r'Co:\s*([+-]?\d*\.\d+|\d+)',    # 匹配Co:后的float数字
}

def list_serial_ports():
    """获取串口列表"""
    ports = serial.tools.list_ports.comports()
    return [(port.device, port.description) for port in ports]

class SerialThread(QThread):
    """串口数据读取线程"""
    data_received = QtCore.pyqtSignal(str)  # 定义信号

    def __init__(self, serial_port):
        super().__init__()
        self.ser = serial_port
        self.main_window = MainWindow()
        self.running = True

    def run(self):
        """线程主函数：持续读取串口数据"""
        while self.running:
            try:
                if self.ser.in_waiting > 0:
                    data = self.ser.readline()  # 读取一行数据
                    if data:
                        try:
                            decoded_data = data.decode('utf-8').strip()
                        except UnicodeDecodeError as e:
                            print(f"解码错误: {e}")
                            decoded_data = ""
                        self.data_received.emit(decoded_data)  # 通过信号传递数据
            except serial.SerialException as e:
                print(f"串口错误: {e}")
                self.main_window.close_serial_port()
                # 处理错误，比如重新打开串口或退出线程
                break

    def stop(self):
        """停止线程"""
        self.running = False
        self.wait()  # 等待线程结束

class BLEThread(QThread):
    update_status_signal = QtCore.pyqtSignal(int)  # 用于发送状态更新的信号
    data_received = QtCore.pyqtSignal(str)  # 定义信号，传递数据

    def __init__(self, mac_address):
        super().__init__()
        self.device_addr = MainWindow.mac_address
        self.notification_characteristic="0000ffe1-0000-1000-8000-00805f9b34fb"
        self.data_str = ""
        self.mainwindow = MainWindow()
        self.client = None
        self.running = True

    # 监听回调函数，此处为打印消息
    def notification_handler(self, characteristic: BleakGATTCharacteristic, data: bytearray):
        try:
            self.data_str += data.decode('utf-8')
            if self.data_str.endswith('\n'):
                print(self.data_str)
                if self.running:
                    self.data_received.emit(self.data_str)  # 通过信号传递数据
                    # self.mainwindow.update_received_data(data=self.data_str)  # 调用解包函数处理接收到的数据
                self.data_str = ""
        except UnicodeDecodeError as e:
            print(f"解码错误: {e}")
            self.data_str = ""

    def disconnected_callback(self, client):
        print("Disconnected callback called!")

    def run(self):
        """在子线程中运行 BLE 连接"""
        while self.running:
            try:
                async def connect_ble():
                    print("starting scan...")

                    # 基于MAC地址查找设备
                    device = await BleakScanner.find_device_by_address(self.device_addr, cb=dict(use_bdaddr=False))
                    if device is None:
                        print(f"Could not find device with address '{self.device_addr}'")
                        return

                    # 事件定义
                    disconnected_event = asyncio.Event()

                    # 创建客户端连接
                    print("connecting to device...")
                    async with BleakClient(device, disconnected_callback=self.disconnected_callback) as client:
                        self.client = client
                        print("Connected")
                        self.update_status_signal.emit(0)  # 发送连接成功的信号
                        await client.start_notify(self.notification_characteristic, self.notification_handler)
                        await disconnected_event.wait()  # 等待直到设备断开连接
                        self.update_status_signal.emit(2)  # 发送断开连接的信号
                        print("BLE disconnected.")

                # 运行异步连接任务
                asyncio.run(connect_ble())
                print("BLE connected.")

            except Exception as e:
                self.update_status_signal.emit(1)  # 发送连接失败的信号
                print(f"BLEThread running error: {e}")

    def get_client(self):
        return self.client

    def get_uuid(self):
        return self.notification_characteristic

    def stop(self):
        """停止线程"""
        # 设置停止标志
        self.running = False
        # 停止线程
        # self.quit()  # 请求线程退出
        # self.wait()  # 等待线程真正结束
        self.terminate()

class BLEScanThread(QThread):
    device_found = QtCore.pyqtSignal(list)  # 用于将设备地址发回 UI
    stop_signal = False  # 用于控制线程停止的标志

    def __init__(self):
        super().__init__()

    def run(self):
        """线程的执行体，扫描 BLE 设备"""
        print("BLE scanning started.")
        while not self.stop_signal:
            devices = asyncio.run(BleakScanner.discover())  # 使用 asyncio.run() 来运行协程
            print(f"Found devices: {devices}")

            # 创建一个设备信息列表，包含设备名称和地址
            device_info_list = []
            for device in devices:
                device_name = device.name if device.name else "未知设备"
                device_address = device.address
                device_info_list.append((device_name, device_address))  # 以元组形式存储设备名称和地址

            # 发射信号，传递设备信息列表
            self.device_found.emit(device_info_list)

            QTimer.singleShot(5000, self.trigger_next_scan)  # 每隔 5 秒扫描一次

    def trigger_next_scan(self):
        """调用此函数继续扫描设备"""
        self.run()

    def stop(self):
        """停止线程的工作"""
        self.stop_signal = True  # 设置标志位为 True，通知线程停止
        self.wait()  # 等待线程完成后再退出


class MainWindow(QMainWindow, Ui_MainWindow):
    mac_address = "00:15:83:00:A5:72"

    def __init__(self):
        super(MainWindow, self).__init__()
        self.ble_thread = None
        self.status_label = None
        self.setupUi(self)
        self.unpacked_data = unpacked_data
        self.populate_ports()  # 填充 Port 下拉菜单
        self.populate_baudrate()  # 填充 Baudrate 下拉菜单
        self.populate_bytesize()  # 填充 Bytesize 下拉菜单
        self.populate_stopbits()  # 填充 Stopbits 下拉菜单
        self.populate_parity()  # 填充 Parity 下拉菜单

        # 连接各个下拉框的信号到相应的槽函数
        self.Port.currentIndexChanged.connect(self.on_port_selection_changed)
        self.Baudrate.currentIndexChanged.connect(self.on_baudrate_changed)
        self.Bytesize.currentIndexChanged.connect(self.on_bytesize_changed)
        self.Stopbits.currentIndexChanged.connect(self.on_stopbits_changed)
        self.Parity.currentIndexChanged.connect(self.on_parity_changed)

        # 连接 SerialBtn 的点击信号到槽函数
        self.SerialBtn.clicked.connect(self.toggle_serial_port)
        # 连接 BLEBtn 的点击信号到槽函数
        self.BLEBtn.clicked.connect(self.BLEBtn_clicked)

        # 串口线程
        self.serial_thread = None
        self.ReceiveData = ""  # 存储接收到的数据

        # 标志串口是否已打开
        self.serial_open = False
        self.ble_open = False

        # 创建场景和视图
        self.scene = QtWidgets.QGraphicsScene()
        self.ModelView.setScene(self.scene)  # 将 QGraphicsView 设置为该场景

        # 加载 SVG 图片并插入到场景
        # self.model_svg_item = QGraphicsSvgItem('.\\img\\model.svg')  # 加载本目录中的 Model.svg
        self.model_svg_item = QGraphicsSvgItem(icon_path)  # 加载本目录中的 Model.svg
        self.scene.addItem(self.model_svg_item)  # 将 SVG 图片添加到场景中

        # 自动缩放图片适应视图
        self.scale_model_to_fit_view()

        # 定时器检查串口变化
        self.port_check_timer = QtCore.QTimer(self)
        self.port_check_timer.timeout.connect(self.check_ports)
        self.port_check_timer.start(5000)  # 每5000ms（5秒）检查一次串口列表

        # 将实例变量放在__init__方法内初始化
        self.ble_window = None

    def BLEBtn_clicked(self):
        if self.ble_open:
            self.disconnect_ble_device()
        else:
            # self.open_ble_window()
            self.connect_ble_device()

    def open_ble_window(self):
        # 创建一个 QDialog 容器并将 BLEWindow 作为 UI 设置
        dialog = QDialog(self)  # 创建 QDialog 作为父窗口的模态对话框
        self.ble_window = BLEWindow()  # 创建 BLEWindow 子窗口实例
        self.ble_window.setupUi(dialog)  # 使用 BLEWindow 的 UI 设置 QDialog

        # 连接 dialog.finished 信号到槽方法
        dialog.finished[int].connect(self.on_ble_dialog_finished)

        # 可选：移除帮助按钮
        dialog.setWindowFlags(dialog.windowFlags() & ~Qt.WindowContextHelpButtonHint)

        # 设置为模态对话框
        dialog.setModal(True)

        # 显示并启动模态对话框
        dialog.exec_()  # 使用 exec_() 来启动模态对话框

    def on_ble_dialog_finished(self):
        """当对话框关闭时，停止 BLE 扫描线程"""
        if self.ble_window:
            self.ble_window.close()
            print("BLEWindow has been closed.")

    def connect_ble_device(self):
        """连接BLE设备并接收串口数据"""
        if MainWindow.mac_address:
            # 置标志为 True
            self.ble_open = True
            # 修改按钮文字为“关闭蓝牙串口”
            self.BLEBtn.setText("关闭蓝牙串口")
            # 禁用 BLEBtn
            self.SerialBtn.setEnabled(False)

            # 创建并启动 BLE 连接线程
            self.ble_thread = BLEThread(MainWindow.mac_address)
            self.ble_thread.update_status_signal.connect(self.BLE_start_status)  # 连接状态更新信号
            self.ble_thread.start()  # 启动 BLE 连接线程

            self.ble_thread.data_received.connect(self.update_received_data)

    # async def stop_ble_notification(self, client, uuid):
    #     await client.stop_notify(uuid)

    def disconnect_ble_device(self):
        """关闭串口"""
        client = self.ble_thread.get_client()
        uuid = self.ble_thread.get_uuid()
        try:
            if self.ble_thread:
                # asyncio.run(self.stop_ble_notification(client, uuid))
                self.ble_thread.stop()  # 停止线程
            print(f"蓝牙串口已关闭")
            self.ble_open = False  # 标记串口已关闭
            # 修改按钮文字为“打开蓝牙串口”
            self.BLEBtn.setText("打开蓝牙串口")
            # 启用 SerialBtn
            self.SerialBtn.setEnabled(True)
            # 更新 ConnectStatus 的 QLabel 控件
            self.ConnectStatus.setText(f"蓝牙断开连接")
            self.ConnectStatus.setStyleSheet("color: red;")  # 设置为红色
        except Exception as e:
            print(f"蓝牙断开时发生错误: {e}")
            self.ConnectStatus.setText(f"蓝牙断开失败")
            self.ConnectStatus.setStyleSheet("color: red;")

    def BLE_start_status(self, status):
        """更新 UI 上的 BLE 连接状态"""
        if status == 0:
            self.ConnectStatus.setText(f"蓝牙已连接")
            self.ConnectStatus.setStyleSheet("color: green;")  # 设置为绿色
        elif status == 1:
            self.ConnectStatus.setText(f"蓝牙连接失败")
            self.ConnectStatus.setStyleSheet("color: red;")
        elif status == 2:
            self.ConnectStatus.setText(f"蓝牙断开连接")
            self.ConnectStatus.setStyleSheet("color: red;")
        else:
            self.ConnectStatus.setText(f"蓝牙连接失败")
            self.ConnectStatus.setStyleSheet("color: red;")

    def scale_model_to_fit_view(self):
        """自动缩放 SVG 图片以适应 QGraphicsView"""
        # 预设已知的尺寸
        svg_width = 84  # SVG 图片的宽度
        # svg_height = 214  # SVG 图片的高度
        scale_factor = 1.0 # 缩放比例

        # 设置缩放比例
        self.model_svg_item.setScale(scale_factor)

        # 如果需要根据缩放后的宽度调整位置，使用下面的代码来居中显示
        new_width = svg_width * scale_factor
        # new_height = svg_height * scale_factor

        # 居中图像
        self.model_svg_item.setPos((self.ModelView.width() - new_width) / 2, 0)

    def update_labels_with_unpacked_data(self, data):
        """更新界面上所有 QLabels 的文本内容"""
        self.Roll.setText(f"{data.Roll:.2f}")
        self.Motor1Speed.setText(f"{data.Motor1Speed:d}")
        self.Motor2Speed.setText(f"{data.Motor2Speed:d}")
        self.ServoAngle.setText(f"{data.ServoAngle:d}")
        self.velKp.setText(f"{data.velKp:.3f}")
        self.velKi.setText(f"{data.velKi:.3f}")
        self.velKd.setText(f"{data.velKd:.3f}")
        self.velOut.setText(f"{data.velOut:2f}")
        self.angleKp.setText(f"{data.angleKp:.3f}")
        self.angleKi.setText(f"{data.angleKi:.3f}")
        self.angleKd.setText(f"{data.angleKi:.3f}")
        self.angleOut.setText(f"{data.angleOut:2f}")
        self.accKp.setText(f"{data.accKp:.3f}")
        self.accKi.setText(f"{data.accKi:.3f}")
        self.accKd.setText(f"{data.accKd:.3f}")
        self.accOut.setText(f"{data.accOut:2f}")

        roll_angle = data.Roll
        self.rotate_model(roll_angle)

    def check_ports(self):
        """检查串口列表是否有变化，并更新 Port 下拉框"""
        available_ports = list_serial_ports()
        current_ports = [self.Port.itemText(i) for i in range(self.Port.count())]

        # 获取所有串口描述符，比较是否有变化
        new_ports = [f"{port} - {description}" for port, description in available_ports]

        if set(current_ports) != set(new_ports):
            # 如果串口列表有变化，重新填充串口列表
            self.populate_ports()

    def populate_ports(self):
        """填充串口列表到ComboBox"""
        ports = list_serial_ports()
        self.Port.clear()  # 清空现有选项
        for port, description in ports:
            self.Port.addItem(f"{port} - {description}", port)

    def populate_baudrate(self):
        """填充波特率列表到ComboBox"""
        baudrates = ['9600', '19200', '38400', '57600', '115200', '230400', '460800', '921600']
        self.Baudrate.clear()
        self.Baudrate.addItems(baudrates)

    def populate_bytesize(self):
        """填充数据位数列表到ComboBox"""
        bytesizes = ['5', '6', '7', '8']
        self.Bytesize.clear()
        self.Bytesize.addItems(bytesizes)

    def populate_stopbits(self):
        """填充停止位列表到ComboBox"""
        stopbits = ['1', '1.5', '2']
        self.Stopbits.clear()
        self.Stopbits.addItems(stopbits)

    def populate_parity(self):
        """填充校验位列表到ComboBox"""
        parities = ['无', '奇校验', '偶校验']
        self.Parity.clear()
        self.Parity.addItems(parities)

    def on_port_selection_changed(self):
        """处理串口选择变化的事件"""
        if self.serial_open:
            print("串口已打开，不能更改端口")
            return  # 如果串口已经打开，禁止更改端口

        selected_port = self.Port.currentData()  # 获取当前选中的串口
        if selected_port:
            ser.port = selected_port  # 设置串口号
            print(f"选中的串口是: {ser.port}")
            # self.open_serial_port()  # 打开串口

    def on_baudrate_changed(self):
        """处理波特率变化的事件"""
        selected_baudrate = self.Baudrate.currentText()  # 获取当前选中的波特率
        if ser.is_open:
            self.close_serial_port()  # 关闭串口
            ser.baudrate = int(selected_baudrate)  # 设置新的波特率
            self.open_serial_port()  # 重新打开串口
        else:
            ser.baudrate = int(selected_baudrate)  # 设置波特率
            print(f"选中的波特率是: {ser.baudrate}")

    def on_bytesize_changed(self):
        """处理数据位数变化的事件"""
        selected_bytesize = self.Bytesize.currentText()  # 获取当前选中的数据位数
        if ser.is_open:
            self.close_serial_port()  # 关闭串口
            ser.bytesize = int(selected_bytesize)  # 设置数据位数
            self.open_serial_port()  # 重新打开串口
        else:
            ser.bytesize = int(selected_bytesize)  # 设置数据位数
            print(f"选中的数据位数是: {ser.bytesize}")

    def on_stopbits_changed(self):
        """处理停止位变化的事件"""
        selected_stopbits = self.Stopbits.currentText()  # 获取当前选中的停止位
        if ser.is_open:
            self.close_serial_port()  # 关闭串口
            if selected_stopbits == '1':
                ser.stopbits = serial.STOPBITS_ONE
            elif selected_stopbits == '1.5':
                ser.stopbits = serial.STOPBITS_ONE_POINT_FIVE
            elif selected_stopbits == '2':
                ser.stopbits = serial.STOPBITS_TWO
            self.open_serial_port()  # 重新打开串口
        else:
            if selected_stopbits == '1':
                ser.stopbits = serial.STOPBITS_ONE
            elif selected_stopbits == '1.5':
                ser.stopbits = serial.STOPBITS_ONE_POINT_FIVE
            elif selected_stopbits == '2':
                ser.stopbits = serial.STOPBITS_TWO
            print(f"选中的停止位是: {ser.stopbits}")

    def on_parity_changed(self):
        """处理校验位变化的事件"""
        selected_parity = self.Parity.currentText()  # 获取当前选中的校验位
        if ser.is_open:
            self.close_serial_port()  # 关闭串口
            if selected_parity == '无':
                ser.parity = 'N'  # 无校验
            elif selected_parity == '奇校验':
                ser.parity = 'O'  # 奇校验
            elif selected_parity == '偶校验':
                ser.parity = 'E'  # 偶校验
            self.open_serial_port()  # 重新打开串口
        else:
            if selected_parity == '无':
                ser.parity = 'N'  # 无校验
            elif selected_parity == '奇校验':
                ser.parity = 'O'  # 奇校验
            elif selected_parity == '偶校验':
                ser.parity = 'E'  # 偶校验
            print(f"选中的校验位是: {ser.parity}")

    def toggle_serial_port(self):
        """切换串口的打开和关闭"""
        if self.serial_open:
            self.close_serial_port()
        else:
            self.open_serial_port()

    def open_serial_port(self):
        """打开串口并进行配置"""
        try:
            ser.timeout = 15  # 设置超时
            ser.open()
            if ser.is_open:
                print(f"串口 {ser.port} 打开成功！")
                self.serial_open = True  # 标记串口已打开
                # 启动串口数据读取线程
                self.serial_thread = SerialThread(ser)
                self.serial_thread.data_received.connect(self.update_received_data)
                self.serial_thread.start()

                # 修改按钮文字为“关闭串口”
                self.SerialBtn.setText("关闭串口")
                # 禁用 BLEBtn
                self.BLEBtn.setEnabled(False)
                # 禁用 Port 下拉框
                self.Port.setEnabled(False)

                # 更新 ConnectStatus 的 QLabel 控件
                self.ConnectStatus.setText(f"{ser.port} 已打开")
                self.ConnectStatus.setStyleSheet("color: green;")  # 设置为绿色
            else:
                print("串口打开失败！")
                self.ConnectStatus.setText(f"{ser.port} 打开失败")
                self.ConnectStatus.setStyleSheet("color: red;")  # 设置为红色
        except Exception as e:
            print(f"串口打开时发生错误: {e}")
            self.ConnectStatus.setText(f"{ser.port} 打开失败")
            self.ConnectStatus.setStyleSheet("color: red;")  # 设置为红色

    def close_serial_port(self):
        """关闭串口"""
        try:
            if self.serial_thread:
                self.serial_thread.stop()  # 停止线程
            ser.close()
            print(f"串口 {ser.port} 已关闭")
            self.serial_open = False  # 标记串口已关闭
            # 修改按钮文字为“打开串口”
            self.SerialBtn.setText("打开串口")
            # 启用 BLEBtn
            self.BLEBtn.setEnabled(True)
            # 启用 Port 下拉框
            self.Port.setEnabled(True)

            # 更新 ConnectStatus 的 QLabel 控件
            self.ConnectStatus.setText(f"{ser.port} 已关闭")
            self.ConnectStatus.setStyleSheet("color: red;")  # 设置为红色
        except Exception as e:
            print(f"关闭串口时发生错误: {e}")
            self.ConnectStatus.setText(f"{ser.port} 关闭失败")
            self.ConnectStatus.setStyleSheet("color: red;")  # 设置为红色

    def update_received_data(self, data):
        """接收到数据并存储"""
        # self.ReceiveData += data + "\n"  # 将接收到的数据添加到 ReceiveData 中
        self.ReceiveData = data  # 覆盖而不是追加数据
        self.process_received_data(self.ReceiveData)  # 调用解包函数处理接收到的数据
        self.ReceiveData = ""  # 清空数据，准备接收新的数据

    def process_received_data(self, data):
        """处理解包逻辑"""
        # 在这里添加你自己的解包逻辑
        print(f"当前接收到的数据: {self.ReceiveData}")
        # 解包代码...
        self.unpacking_data(data)
        self.update_labels_with_unpacked_data(self.unpacked_data)

    def unpacking_data(self, data):
        for attribute, regex in pattern.items():
            match = re.search(regex, data)
            if match:  # 只有匹配成功时，才进行值的提取和转换
                value = match.group(1)
                # 将匹配的值转换为float或int后，更新self.unpacked_data的相应属性
                if '.' in value:
                    setattr(self.unpacked_data, attribute, float(value))
                else:
                    setattr(self.unpacked_data, attribute, int(value))
            else:
                # 如果没有匹配到，决定是否为属性赋一个默认值
                setattr(self.unpacked_data, attribute, 0)  # 或者使用其他默认值

    def rotate_model(self, angle):
        """旋转并缩放 Model.svg 图片，使其适应 QGraphicsView，并围绕中心点旋转"""

        # 获取图片的中心点
        rect = self.model_svg_item.boundingRect()
        center_x = rect.center().x()
        center_y = rect.center().y()

        # 设置旋转的原点为图片的中心
        self.model_svg_item.setTransformOriginPoint(center_x, center_y)

        # 旋转图片
        self.model_svg_item.setRotation(angle)

        print(f"Model 图像已旋转到 {angle} 度，并缩放到适应视图")


class BLEWindow(QMainWindow, Ui_BLEWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 设置UI
        print("BLEWindow initialized.")
        self.listWidget.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)

        # 连接 listWidget 的 itemClicked 信号
        self.listWidget.itemDoubleClicked.connect(self.on_item_clicked)
        self.SearchBLE.clicked.connect(self.search_ble_devices)

        # 创建并启动 BLE 扫描线程
        self.ble_scan_thread = BLEScanThread()
        self.ble_scan_thread.device_found.connect(self.add_device_to_list)
        self.ble_scan_thread.start()
        print("BLE scan thread started.")

    def add_device_to_list(self, device_info_list):
        """更新设备列表，格式为 '设备名称 - MAC地址'"""
        try:
            # 清空当前列表
            self.listWidget.clear()

            for device_name, device_address in device_info_list:
                # 如果设备名称为空，使用“未知设备”
                if not device_name:
                    device_name = "未知设备"
                # 如果设备名称长度大于20个字符，则截断并添加“...”
                elif len(device_name) > 20:
                    device_name = device_name[:20] + "..."

                # 将设备名称和地址以 '名称 - MAC地址' 格式添加到列表中
                display_text = f"{device_name} - {device_address}"
                self.listWidget.addItem(display_text)
        except Exception as e:
            print(f"更新设备列表时发生错误: {e}")

    def on_item_clicked(self, item):
        """处理双击列表项的操作"""
        if item.isSelected():  # 判断项是否选中
            from PyQt5.QtWidgets import QMessageBox
            QMessageBox.information(None, "提示", "您选择的是：" + item.text(), QMessageBox.Ok)
        # 打印并返回对应的device_address
        device_info = item.text()
        print(f"点击了设备: {device_info}")

    def closeEvent(self, event):
        """关闭窗口时停止线程"""
        print("closeEvent triggered.")
        if self.ble_scan_thread and not self.ble_scan_thread.stop_signal:
            self.ble_scan_thread.stop()  # 停止扫描线程
        event.accept()

    def search_ble_devices(self):
        """启动或停止 BLE 设备搜索的逻辑"""
        # 获取MAC1~6的输入值，拼成MAC地址
        mac1 = self.MAC1.text()
        mac2 = self.MAC2.text()
        mac3 = self.MAC3.text()
        mac4 = self.MAC4.text()
        mac5 = self.MAC5.text()
        mac6 = self.MAC6.text()
        mac_address = f"{mac1}:{mac2}:{mac3}:{mac4}:{mac5}:{mac6}"
        print(f"搜索的MAC地址是: {mac_address}")
        MainWindow.mac_address = mac_address  # 将MAC地址存储到MainWindow类的类变量中



def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
