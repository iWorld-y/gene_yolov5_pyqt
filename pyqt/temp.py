# encoding=gbk
import sys
import cv2
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QPushButton


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        # ���������ڱ���ͳߴ�
        self.setWindowTitle('Camera Viewer')
        self.setGeometry(100, 100, 640, 480)

        # ���� QLabel ���������ʾ����ͷ����
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 640, 480)

        # ������ͣ��ť
        self.pause_button = QPushButton('Pause', self)
        self.pause_button.setGeometry(280, 450, 80, 30)
        self.pause_button.clicked.connect(self.toggle_pause)

        # ��ʼ������ͷ
        self.cap = cv2.VideoCapture(0)

        # ������ʱ�������ڸ��»���
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_frame)
        self.timer.start(50)

        # ��ʶ��ǰ�Ƿ�����ͣ״̬
        self.paused = False

    def update_frame(self):
        # ���������ͣ״̬��ֱ�ӷ���
        if self.paused:
            return

        # ��ȡ����ͷ���沢���䷭ת
        ret, frame = self.cap.read()
        frame = cv2.flip(frame, 1)
        # ������ɫ
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        height, width, channel = frame.shape

        # ���� QImage ���󣬲�������ͷ�����л�ȡ��������
        qimage = QImage(frame, width, height, channel * width, QImage.Format_RGB888)

        # �� QImage ����ת��Ϊ QPixmap ���󣬲���ʾ�� QLabel �����
        pixmap = QPixmap(qimage)
        self.label.setPixmap(pixmap)

    def toggle_pause(self):
        self.paused = not self.paused


app = QApplication(sys.argv)
win = MainWindow()
win.show()
sys.exit(app.exec_())
