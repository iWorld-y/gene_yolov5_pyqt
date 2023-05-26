# encoding=gbk
import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # 设置主窗口标题和尺寸
        self.setWindowTitle('Camera Viewer')
        self.setGeometry(100, 100, 640, 480)

        # 创建 QLabel 组件用于显示摄像头画面
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 640, 480)

        # 创建暂停按钮
        self.pause_button = QPushButton('Pause', self)
        self.pause_button.setGeometry(280, 450, 80, 30)
        self.pause_button.clicked.connect(self.toggle_pause)

        # 初始化摄像头
        self.cap = cv2.VideoCapture(0)

        # 创建定时器，用于更新画面
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)

        # 标识当前是否处于暂停状态
        self.paused = False

    def update_frame(self):
        # 如果处于暂停状态，直接返回
        if self.paused:
            return

        # 读取摄像头画面并将其翻转
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        # 矫正颜色
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape

        # 创建 QImage 对象，并从摄像头画面中获取像素数据
        qimage = QImage(frame, width, height, channel * width, QImage.Format_RGB888)

        # 将 QImage 对象转换为 QPixmap 对象，并显示在 QLabel 组件上
        pixmap = QPixmap(qimage)
        self.label.setPixmap(pixmap)

    def toggle_pause(self):
        self.paused = not self.paused


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
