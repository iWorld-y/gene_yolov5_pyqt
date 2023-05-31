# %%
import onnxruntime
import logging
import cv2
import numpy as np
import matplotlib.pyplot as plt

logging.basicConfig(format='%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s: %(message)s',
                    level=logging.DEBUG)


# %%
class YOLOV5():
    def __init__(self, onnxpath):
        self.onnx_session = onnxruntime.InferenceSession(onnxpath, providers=["CPUExecutionProvider"])
        self.input_name = self.get_input_name()
        self.output_name = self.get_output_name()

    # -------------------------------------------------------
    #   获取输入输出的名字
    # -------------------------------------------------------
    def get_input_name(self):
        input_name = []
        for node in self.onnx_session.get_inputs():
            input_name.append(node.name)
        return input_name

    def get_output_name(self):
        output_name = []
        for node in self.onnx_session.get_outputs():
            output_name.append(node.name)
        return output_name

    # -------------------------------------------------------
    #   输入图像
    # -------------------------------------------------------
    def get_input_feed(self, img_tensor):
        input_feed = {}
        for name in self.input_name:
            input_feed[name] = img_tensor
        return input_feed

    # -------------------------------------------------------
    #   1.cv2读取图像并resize
    #	2.图像转BGR2RGB和HWC2CHW
    #	3.图像归一化
    #	4.图像增加维度
    #	5.onnx_session 推理
    # -------------------------------------------------------
    def inference(self, img_path):
        img = cv2.imread(img_path)
        or_img = cv2.resize(img, (640, 640))
        img = or_img[:, :, ::-1].transpose(2, 0, 1)  # BGR2RGB和HWC2CHW
        img = img.astype(dtype=np.float32)
        img /= 255.0
        img = np.expand_dims(img, axis=0)
        input_feed = self.get_input_feed(img)
        pred = self.onnx_session.run(None, input_feed)[0]
        return pred, or_img


# %%
# image_path = r"E:\BaiduNetdiskDownload\Deepfashion2\Deepfashion2\train\092745.jpg"
image_path = r"E:\BaiduNetdiskDownload\Deepfashion2\Deepfashion2\train\134526.jpg"
# image_path = r"E:\BaiduNetdiskDownload\Deepfashion2\Deepfashion2\train\045632.jpg"
# image_path = r"E:\BaiduNetdiskDownload\Deepfashion2\Deepfashion2\train\134562.jpg"
# %%
onnx_path = r"D:\CodeProject\gene_yolov5_pyqt\pyqt\v5.onnx"
yolo = YOLOV5(onnx_path)
# %%
yolo_img = yolo.inference(image_path)
# %%
plt.imshow(cv2.cvtColor(yolo_img[1], cv2.COLOR_BGR2RGB))
plt.show()
plt.imshow(plt.imread(image_path))
plt.show()
