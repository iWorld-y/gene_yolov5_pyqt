import sys
from PyQt5.QtWidgets import QApplication, QWidget, QSlider, QVBoxLayout, QLabel


class Example(QWidget):

    def __init__(self):
        super().__init__()

        self.initUI()

    def initUI(self):
        vbox = QVBoxLayout()

        sld = QSlider()
        sld.setMinimum(0)
        sld.setMaximum(100)
        sld.setValue(50)
        sld.setTickInterval(10)
        sld.setTickPosition(QSlider.TicksBothSides)

        sld.valueChanged[int].connect(self.changeValue)

        self.label = QLabel('IoU: 50', self)

        vbox.addWidget(sld)
        vbox.addWidget(self.label)

        self.setLayout(vbox)

        self.setGeometry(300, 300, 250, 150)
        self.setWindowTitle('QSlider')
        self.show()

    def changeValue(self, value):
        self.label.setText(f"IoU: {value}")


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = Example()
    sys.exit(app.exec_())
