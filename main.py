# -*- coding: utf-8 -*-

import sys
import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QMainWindow
from PyQt5 import QtWidgets, QtCore
from mainWindow import Ui_MainWindow
from PyQt5.QtSvg import QGraphicsSvgItem
from PyQt5.QtCore import Qt


ser = serial.Serial()
class UnpackedData:
    def __init__(self):
        self.Roll = 0.0
        self.Motor1Speed = 0.0
        self.Motor2Speed = 0.0
        self.ServoAngle = 0.0
        self.VerticalKp = 0.0
        self.VerticalKi = 0.0
        self.VerticalKd = 0.0
        self.VerticalOut = 0.0
        self.VelocityKp = 0.0
        self.VelocityKi = 0.0
        self.VelocityOut = 0.0
# 创建UnpackedData实例
unpacked_data = UnpackedData()

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
        self.running = True

    def run(self):
        """线程主函数：持续读取串口数据"""
        while self.running:
            if self.ser.in_waiting > 0:
                data = self.ser.readline()  # 读取一行数据
                if data:
                    decoded_data = data.decode('utf-8').strip()
                    self.data_received.emit(decoded_data)  # 通过信号传递数据

    def stop(self):
        """停止线程"""
        self.running = False
        self.wait()  # 等待线程结束


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
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

    def scale_model_to_fit_view(self):
        """自动缩放 SVG 图片以适应 QGraphicsView"""
        # 预设已知的尺寸
        svg_width = 351  # SVG 图片的宽度
        svg_height = 892  # SVG 图片的高度
        view_height = self.ModelView.height()  # 获取 ModelView 的高度

        # 计算缩放比例：我们让图片的高度占满 ModelView
        scale_factor = view_height / svg_height

        # 设置缩放比例
        self.model_svg_item.setScale(scale_factor)

        # 如果需要根据缩放后的宽度调整位置，使用下面的代码来居中显示
        new_width = svg_width * scale_factor
        new_height = svg_height * scale_factor

        # 居中图像 (如果需要)
        self.model_svg_item.setPos((self.ModelView.width() - new_width) / 2, 0)

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
            self.open_serial_port()  # 打开串口

    def on_baudrate_changed(self):
        """处理波特率变化的事件"""
        selected_baudrate = self.Baudrate.currentText()  # 获取当前选中的波特率
        ser.baudrate = int(selected_baudrate)  # 设置波特率
        print(f"选中的波特率是: {ser.baudrate}")

    def on_bytesize_changed(self):
        """处理数据位数变化的事件"""
        selected_bytesize = self.Bytesize.currentText()  # 获取当前选中的数据位数
        ser.bytesize = int(selected_bytesize)  # 设置数据位数
        print(f"选中的数据位数是: {ser.bytesize}")

    def on_stopbits_changed(self):
        """处理停止位变化的事件"""
        selected_stopbits = self.Stopbits.currentText()  # 获取当前选中的停止位
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
            if ser.isOpen():
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
            self.update_connect_status_failure(f"{ser.port} 打开失败: {e}")

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
        print(f"接收到的数据: {data}")
        self.ReceiveData += data + "\n"  # 将接收到的数据添加到 ReceiveData 中
        self.process_received_data()  # 调用解包函数处理接收到的数据

    def process_received_data(self):
        """处理解包逻辑"""
        # 在这里添加你自己的解包逻辑
        print(f"当前接收到的数据: {self.ReceiveData}")
        # 解包代码...
        # 例如：
        # result = your_unpacking_function(self.ReceiveData)
        roll_angle = unpacked_data.Roll  # 获取 Roll 角度

        # 将图片旋转到 unpacked_data.Roll 角度
        self.rotate_model(roll_angle)
        # self.ReceiveData = ""  # 清空数据，准备接收新的数据

    def rotate_model(self, angle):
        """旋转 Model.svg 图片到指定的角度"""
        # 旋转图片：QGraphicsSvgItem 的 setRotation 方法接受角度值
        self.model_svg_item.setRotation(angle)
        print(f"Model 图像已旋转到 {angle} 度")

def main():
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling)
    app = QtWidgets.QApplication(sys.argv)
    main_window = MainWindow()
    main_window.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    main()
