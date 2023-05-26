# encoding=gbk
import os
import cv2
import numpy as np
import onnxruntime
import time

CLASSES = ["short sleeve top", "long sleeve top", "short sleeve outwear", "long sleeve outwear", "vest", "sling",
           "shorts", "trousers", "skirt", "short sleeve dress", "long sleeve dress", "vest dress",
           "sling dress"]  # coco80���


class YOLOV5():
    def __init__(self, onnxpath):
        self.onnx_session = onnxruntime.InferenceSession(onnxpath, providers=['CPUExecutionProvider'])
        self.model_input_names = self.get_model_input_names()
        self.model_output_names = self.get_model_output_names()

    # -------------------------------------------------------
    #   ��ȡ�������������
    # -------------------------------------------------------
    def get_model_input_names(self):
        """
        ��ȡONNXģ�͵�����ڵ������б�

        ����ֵ��
            input_name: ������������ڵ����Ƶ��б�
        """
        input_name = []
        for node in self.onnx_session.get_inputs():
            input_name.append(node.name)
        return input_name

    def get_model_output_names(self):
        """
        ��ȡONNXģ�͵�����ڵ������б�

        ����ֵ��
            output_name: ������������ڵ����Ƶ��б�
        """
        output_name = []
        for node in self.onnx_session.get_outputs():
            output_name.append(node.name)
        return output_name

    # -------------------------------------------------------
    #   ����ͼ��
    # -------------------------------------------------------
    def get_input_feed(self, img_tensor):
        input_feed = {}
        for name in self.model_input_names:
            input_feed[name] = img_tensor
        return input_feed

    # -------------------------------------------------------
    #   1.cv2��ȡͼ��resize
    #   2.ͼ��תBGR2RGB��HWC2CHW
    #   3.ͼ���һ��
    #   4.ͼ������ά��
    #   5.onnx_session ����
    # -------------------------------------------------------
    def inference(self, img_path):
        img = cv2.imread(img_path)
        img_o = img.copy()
        or_img = cv2.resize(img, (640, 640))
        img = or_img[:, :, ::-1].transpose(2, 0, 1)  # BGR2RGB��HWC2CHW
        img = img.astype(dtype=np.float32)
        img /= 255.0
        img = np.expand_dims(img, axis=0)
        input_feed = self.get_input_feed(img)
        pred = self.onnx_session.run(None, input_feed)[0]
        return pred, img_o


# dets:  array [x,6] 6��ֵ�ֱ�Ϊx1,y1,x2,y2,score,class
# thresh: ��ֵ
def nms(dets, thresh):
    x1 = dets[:, 0]
    y1 = dets[:, 1]
    x2 = dets[:, 2]
    y2 = dets[:, 3]
    # -------------------------------------------------------
    #   ���������
    #   ���ŶȴӴ�С����
    # -------------------------------------------------------
    areas = (y2 - y1 + 1) * (x2 - x1 + 1)
    scores = dets[:, 4]
    keep = []
    index = scores.argsort()[::-1]

    while index.size > 0:
        i = index[0]
        keep.append(i)
        # -------------------------------------------------------
        #   �����ཻ���
        #   1.�ཻ
        #   2.���ཻ
        # -------------------------------------------------------
        x11 = np.maximum(x1[i], x1[index[1:]])
        y11 = np.maximum(y1[i], y1[index[1:]])
        x22 = np.minimum(x2[i], x2[index[1:]])
        y22 = np.minimum(y2[i], y2[index[1:]])

        w = np.maximum(0, x22 - x11 + 1)
        h = np.maximum(0, y22 - y11 + 1)

        overlaps = w * h
        # -------------------------------------------------------
        #   ����ÿ����������IOU��ȥ�����ظ��Ŀ򣬼�IOUֵ��Ŀ�
        #   IOUС��thresh�Ŀ�������
        # -------------------------------------------------------
        ious = overlaps / (areas[i] + areas[index[1:]] - overlaps)
        idx = np.where(ious <= thresh)[0]
        index = index[idx + 1]
    return keep


def xywh2xyxy(x):
    # [x, y, w, h] to [x1, y1, x2, y2]
    y = np.copy(x)
    y[:, 0] = x[:, 0] - x[:, 2] / 2
    y[:, 1] = x[:, 1] - x[:, 3] / 2
    y[:, 2] = x[:, 0] + x[:, 2] / 2
    y[:, 3] = x[:, 1] + x[:, 3] / 2
    return y


def filter_box(org_box, conf_thres, iou_thres):  # ���˵����õĿ�
    # -------------------------------------------------------
    #   ɾ��Ϊ1��ά��
    #   ɾ�����Ŷ�С��conf_thres��BOX
    # -------------------------------------------------------
    org_box = np.squeeze(org_box)
    conf = org_box[..., 4] > conf_thres
    box = org_box[conf == True]
    # -------------------------------------------------------
    #   ͨ��argmax��ȡ���Ŷ��������
    # -------------------------------------------------------
    cls_cinf = box[..., 5:]
    cls = []
    for i in range(len(cls_cinf)):
        cls.append(int(np.argmax(cls_cinf[i])))
    all_cls = list(set(cls))
    # -------------------------------------------------------
    #   �ֱ��ÿ�������й���
    #   1.����6��Ԫ���滻Ϊ����±�
    #   2.xywh2xyxy ����ת��
    #   3.�����Ǽ������ƺ������BOX�±�
    #   4.�����±�ȡ���Ǽ������ƺ��BOX
    # -------------------------------------------------------
    output = []

    for i in range(len(all_cls)):
        curr_cls = all_cls[i]
        curr_cls_box = []
        curr_out_box = []
        for j in range(len(cls)):
            if cls[j] == curr_cls:
                box[j][5] = curr_cls
                curr_cls_box.append(box[j][:6])
        curr_cls_box = np.array(curr_cls_box)
        # curr_cls_box_old = np.copy(curr_cls_box)
        curr_cls_box = xywh2xyxy(curr_cls_box)
        curr_out_box = nms(curr_cls_box, iou_thres)
        for k in curr_out_box:
            output.append(curr_cls_box[k])
    output = np.array(output)
    return output


def draw(image, box_data):
    # -------------------------------------------------------
    #   ȡ�������㻭��
    # -------------------------------------------------------
    boxes = box_data[..., :4].astype(np.int32)
    scores = box_data[..., 4]
    classes = box_data[..., 5].astype(np.int32)

    img_height_o = image.shape[0]
    img_width_o = image.shape[1]
    x_ratio = img_width_o / 640
    y_ratio = img_height_o / 640

    for box, score, cl in zip(boxes, scores, classes):
        top, left, right, bottom = box
        print('class: {}, score: {}'.format(CLASSES[cl], score))
        print('box coordinate left,top,right,down: [{}, {}, {}, {}]'.format(top, left, right, bottom))

        top = int(top * x_ratio)
        right = int(right * x_ratio)
        left = int(left * y_ratio)
        bottom = int(bottom * y_ratio)

        cv2.rectangle(image, (top, left), (right, bottom), (255, 0, 0), 2)
        cv2.putText(image, '{0} {1:.2f}'.format(CLASSES[cl], score),
                    (top, left),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.6, (0, 0, 255), 2)


if __name__ == "__main__":
    onnx_path = "/home/eugene/code/Multi-labelClothingDetection/runs/v5/exp2/weights/best.onnx"
    model = YOLOV5(onnx_path)  # ģ�͵����85��ɣ�x��y��w��h��ǰ���÷֡�80�����
    output, or_img = model.inference('/home/eugene/code/gene_yolov5_pyqt/pyqt/temp/test.jpg')
    outbox = filter_box(output, 0.5, 0.5)
    draw(or_img, outbox)
    cv2.imwrite('/home/eugene/code/gene_yolov5_pyqt/pyqt/temp/res.jpg', or_img)
