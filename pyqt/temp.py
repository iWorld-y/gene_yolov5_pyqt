import numpy as np
import cv2

import sys
import cv2
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel

class VideoPlayer(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Video Player")
        self.setGeometry(100, 100, 640, 480)

        # 创建标签用于显示视频画面
        self.label = QLabel(self)
        self.label.setGeometry(0, 0, 640, 480)

        # 打开视频文件
        self.cap  = cv2.VideoCapture('/home/eugene/autodl-tmp/test/1.mp4')

        # 开始播放视频
        self.timer = QTimer()
        self.timer.timeout.connect(self.play_video)
        self.timer.start(30)

    def play_video(self):
        # 读取一帧视频
        ret, frame = self.cap.read()

        # 如果成功读取到了一帧视频
        if ret:
            # 将图像格式从OpenCV格式转换为QImage格式
            image = QImage(frame.data, frame.shape[1], frame.shape[0], QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(image)

            # 在标签上显示图像
            self.label.setPixmap(pixmap)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer()
    player.show()
    sys.exit(app.exec_())

