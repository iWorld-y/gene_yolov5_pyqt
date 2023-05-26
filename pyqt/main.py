import logging
import os
import sys

from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog
from MainWindow import *


class Gene_Window(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(Gene_Window, self).__init__(parent)
        self.main_ui = Ui_MainWindow()
        self.main_ui.setupUi(self)
        self.init_clicked()

    def init_clicked(self):
        self.main_ui.open_weight.clicked.connect(self.open_weight)

    def open_weight(self):
        self.weight_path, _ = QFileDialog.getOpenFileName(self.main_ui.open_weight, "选择权重",
                                                          '/home/eugene/code/Multi-labelClothingDetection/runs/v5/exp2',
                                                          "*.pt")
        if not self.weight_path:
            QtWidgets.QMessageBox.warning(self, "错误", "未选择权重", buttons=QtWidgets.QMessageBox.Ok,
                                          defaultButton=QtWidgets.QMessageBox.Ok)
            self.main_ui.open_weight.setText(
                QtCore.QCoreApplication.translate("MainWindow", "选择权重"))
            return

        weight_name = os.path.basename(self.weight_path)
        logging.info(f"已获取 weight:\t{weight_name}")
        self.main_ui.open_weight.setText(
            QtCore.QCoreApplication.translate("MainWindow", f"当前权重：\n{weight_name}"))

    def model_init(self):
        self.weight_path = "runs/v5/exp2/weights/best.pt"
        self.device = '0'  # 选取 GPU 0
        self.img_size = 640
        self.augment = 640

    def openimage(self):
        # self.imgName, imgType = QFileDialog.getOpenFileName(self, "打开图片", "", "*.jpg;;*.png;;All Files(*)")
        # jpg = QtGui.QPixmap(self.imgName).scaled(self.showImage.width(), self.showImage.height())
        # self.showImage.setPixmap(jpg)
        pass


if __name__ == '__main__':

    logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                        level=logging.DEBUG)
    app = QApplication(sys.argv)
    myWin = Gene_Window()
    myWin.show()
    if (os.path.exists(os.path.join(yolo_project_path, yolo_name))):
        os.system(f"rm -rf {os.path.join(yolo_project_path, yolo_name)}")
    sys.exit(app.exec_())
