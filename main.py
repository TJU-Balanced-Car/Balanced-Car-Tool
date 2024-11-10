# -*- coding: utf-8 -*-

import sys
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QMainWindow, QDialog
from PyQt5 import QtWidgets, QtCore
from mainWindow import Ui_MainWindow
from BLEWindow import Ui_Form as Ui_BLEWindow
from PyQt5.QtSvg import QGraphicsSvgItem
import re
import asyncio
from bleak import BleakScanner


ser = serial.Serial()
class UnpackedData:
    def __init__(self):
        self.Roll = 0.0
        self.Motor1Speed = 0
        self.Motor2Speed = 0
        self.ServoAngle = 0
        self.VerticalKp = 0.0
        self.VerticalKi = 0.0
        self.VerticalKd = 0.0
        self.VerticalOut = 0
        self.VelocityKp = 0.0
        self.VelocityKi = 0.0
        self.VelocityOut = 0
# 创建UnpackedData实例
unpacked_data = UnpackedData()
# 正则表达式匹配模式
pattern = {
    'Roll': r'R:\s*([+-]?\d*\.\d+|\d+)',  # 匹配R:后面的float数字
    'Motor1Speed': r'M1:\s*(\d+)',         # 匹配M1:后面的int数字
    'Motor2Speed': r'M2:\s*(\d+)',         # 匹配M2:后面的int数字
    'ServoAngle': r'S:\s*(\d+)',           # 匹配S:后面的int数字
    'VerticalKp': r'Lp:\s*([+-]?\d*\.\d+|\d+)',  # 匹配Lp:后的float数字
    'VerticalKi': r'Li:\s*([+-]?\d*\.\d+|\d+)',  # 匹配Li:后的float数字
    'VerticalKd': r'Ld:\s*([+-]?\d*\.\d+|\d+)',  # 匹配Ld:后的float数字
    'VerticalOut': r'Lo:\s*(\d+)',         # 匹配Lo:后的int数字
    'VelocityKp': r'Yp:\s*([+-]?\d*\.\d+|\d+)',  # 匹配Yp:后的float数字
    'VelocityKi': r'Yi:\s*([+-]?\d*\.\d+|\d+)',  # 匹配Yi:后的float数字
    'VelocityOut': r'Yo:\s*(\d+)'          # 匹配Yo:后的int数字
}

def list_serial_ports():
    """获取串口列表"""
    ports = serial.tools.list_ports.comports()
    return [(port.device, port.description) for port in ports]

class SerialThread(QtCore.QThread):
    """串口数据读取线程"""
    data_received = QtCore.pyqtSignal(str)  # 定义信号

    def __init__(self, ser):
        super().__init__()
        self.ser = ser
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


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
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
        self.BLEBtn.clicked.connect(self.open_ble_window)

        # 串口线程
        self.serial_thread = None
        self.ReceiveData = ""  # 存储接收到的数据

        # 标志串口是否已打开
        self.serial_open = False

        # 创建场景和视图
        self.scene = QtWidgets.QGraphicsScene()
        self.ModelView.setScene(self.scene)  # 将 QGraphicsView 设置为该场景

        # 加载 SVG 图片并插入到场景
        self.model_svg_item = QGraphicsSvgItem('model.svg')  # 加载本目录中的 Model.svg
        self.scene.addItem(self.model_svg_item)  # 将 SVG 图片添加到场景中

        # 自动缩放图片适应视图
        self.scale_model_to_fit_view()

        # 定时器检查串口变化
        self.port_check_timer = QtCore.QTimer(self)
        self.port_check_timer.timeout.connect(self.check_ports)
        self.port_check_timer.start(5000)  # 每5000ms（5秒）检查一次串口列表

        # 将实例变量放在__init__方法内初始化
        self.ui_ble_window = None
        self.ble_window = None

    def open_ble_window(self):
        # 打开 BLEWindow 子窗口
        self.ble_window = QDialog()  # 可以根据需要修改为QDialog或QMainWindow
        self.ui_ble_window = Ui_BLEWindow()  # 创建BLEWindow实例
        self.ui_ble_window.setupUi(self.ble_window)  # 设置UI
        self.ble_window.show()  # 显示BLE窗口

    def scale_model_to_fit_view(self):
        """自动缩放 SVG 图片以适应 QGraphicsView"""
        # 预设已知的尺寸
        svg_width = 84  # SVG 图片的宽度
        svg_height = 214  # SVG 图片的高度

        scale_factor = 1.0

        # 设置缩放比例
        self.model_svg_item.setScale(scale_factor)

        # 如果需要根据缩放后的宽度调整位置，使用下面的代码来居中显示
        new_width = svg_width * scale_factor
        # new_height = svg_height * scale_factor

        # 居中图像
        self.model_svg_item.setPos((self.ModelView.width() - new_width) / 2, 0)

    def update_labels_with_unpacked_data(self, unpacked_data):
        """更新界面上所有 QLabels 的文本内容"""
        self.Roll.setText(f"{unpacked_data.Roll:.2f}")
        self.Motor1Speed.setText(f"{unpacked_data.Motor1Speed}")
        self.Motor2Speed.setText(f"{unpacked_data.Motor2Speed}")
        self.ServoAngle.setText(f"{unpacked_data.ServoAngle}")
        self.VerticalKp.setText(f"{unpacked_data.VerticalKp:.2f}")
        self.VerticalKi.setText(f"{unpacked_data.VerticalKi:.2f}")
        self.VerticalKd.setText(f"{unpacked_data.VerticalKd:.2f}")
        self.VerticalOut.setText(f"{unpacked_data.VerticalOut}")
        self.VelocityKp.setText(f"{unpacked_data.VelocityKp:.2f}")
        self.VelocityKi.setText(f"{unpacked_data.VelocityKi:.2f}")
        self.VelocityOut.setText(f"{unpacked_data.VelocityOut}")

        roll_angle = unpacked_data.Roll
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
                self.update_connect_status_failure(f"{ser.port} 打开失败")
        except Exception as e:
            print(f"串口打开时发生错误: {e}")
            self.update_connect_status_failure(f"{ser.port} 打开失败")

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
            self.update_connect_status_failure(f"{ser.port} 关闭失败: {e}")

    def update_connect_status_failure(self, message):
        """更新 ConnectStatus 显示失败消息"""
        self.ConnectStatus.setText(message)
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


def on_item_clicked(item):
    """当点击 listWidget 中的项时输出其 MAC 地址"""
    mac_address = item.text()
    print(f"Item clicked: {mac_address}")
    return mac_address

class BLEWindow(QMainWindow, Ui_BLEWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)  # 设置UI
        self.listWidget.itemClicked.connect(on_item_clicked)  # 绑定点击事件

        # 启动异步扫描
        self.loop = asyncio.get_event_loop()
        self.loop.create_task(self.scan_ble_devices())

    async def scan_ble_devices(self):
        """扫描附近的 BLE 设备，并将设备 MAC 地址添加到 listWidget 中"""
        while True:
            devices = await BleakScanner.discover()  # 获取附近的 BLE 设备
            for device in devices:
                if device.address not in [self.listWidget.item(i).text() for i in range(self.listWidget.count())]:
                    self.listWidget.addItem(device.address)  # 将设备的 MAC 地址添加到 listWidget
            await asyncio.sleep(5)  # 每隔 5 秒扫描一次


def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
