from aip import AipBodyAnalysis
import sys


import cv2
import os
import config as cfg
import base64
import time


def pose_analyse(img, dic):
    nose = (int(dic['nose']['x']), int(dic['nose']['y']))
    neck = (int(dic['neck']['x']), int(dic['neck']['y']))
    if (neck[1] <= nose[1]):
        return 'warn'
    return 'ok'


def draw_line(img, dic, text):
    color = (0, 255, 0)
    thickness = 2
    if (text == 'warn'):
        color = (0, 0, 255)

    # nose ---> neck
    cv2.line(img, (int(dic['nose']['x']), int(dic['nose']['y'])), (int(dic['neck']['x']), int(dic['neck']['y'])), color,
             thickness)
    # neck --> left_shoulder
    cv2.line(img, (int(dic['neck']['x']), int(dic['neck']['y'])),
             (int(dic['left_shoulder']['x']), int(dic['left_shoulder']['y'])), color, thickness)
    # neck --> right_shoulder
    cv2.line(img, (int(dic['neck']['x']), int(dic['neck']['y'])),
             (int(dic['right_shoulder']['x']), int(dic['right_shoulder']['y'])), color, thickness)
    # left_shoulder --> left_elbow
    cv2.line(img, (int(dic['left_shoulder']['x']), int(dic['left_shoulder']['y'])),
             (int(dic['left_elbow']['x']), int(dic['left_elbow']['y'])), color, thickness)
    # left_elbow --> left_wrist
    cv2.line(img, (int(dic['left_elbow']['x']), int(dic['left_elbow']['y'])),
             (int(dic['left_wrist']['x']), int(dic['left_wrist']['y'])), color, thickness)
    # right_shoulder --> right_elbow
    cv2.line(img, (int(dic['right_shoulder']['x']), int(dic['right_shoulder']['y'])),
             (int(dic['right_elbow']['x']), int(dic['right_elbow']['y'])), color, thickness)
    # right_elbow --> right_wrist
    cv2.line(img, (int(dic['right_elbow']['x']), int(dic['right_elbow']['y'])),
             (int(dic['right_wrist']['x']), int(dic['right_wrist']['y'])), color, thickness)
    # neck --> left_hip
    cv2.line(img, (int(dic['neck']['x']), int(dic['neck']['y'])),
             (int(dic['left_hip']['x']), int(dic['left_hip']['y'])), color, thickness)
    # neck --> right_hip
    cv2.line(img, (int(dic['neck']['x']), int(dic['neck']['y'])),
             (int(dic['right_hip']['x']), int(dic['right_hip']['y'])), color, thickness)
    # left_hip --> left_knee
    cv2.line(img, (int(dic['left_hip']['x']), int(dic['left_hip']['y'])),
             (int(dic['left_knee']['x']), int(dic['left_knee']['y'])), color, thickness)
    # right_hip --> right_knee
    cv2.line(img, (int(dic['right_hip']['x']), int(dic['right_hip']['y'])),
             (int(dic['right_knee']['x']), int(dic['right_knee']['y'])), color, thickness)
    # left_knee --> left_ankle
    cv2.line(img, (int(dic['left_knee']['x']), int(dic['left_knee']['y'])),
             (int(dic['left_ankle']['x']), int(dic['left_ankle']['y'])), color, thickness)
    # right_knee --> right_ankle
    cv2.line(img, (int(dic['right_knee']['x']), int(dic['right_knee']['y'])),
             (int(dic['right_ankle']['x']), int(dic['right_ankle']['y'])), color, thickness)


def draw_point(img, dic, text):
    color = (0, 255, 0)
    thickness = 2
    if (text == 'warn'):
        color = (0, 0, 255)
    for i in dic:
        cv2.circle(img, (int(dic[i]['x']), int(dic[i]['y'])), 5, color, thickness)


def draw_box(img, dic, text):
    color = (255, 0, 0)
    if (text == 'warn'):
        color = (0, 0, 255)

    left_top = (int(dic['left']), int(dic['top']))
    left_bottom = (int(dic['left']), int(dic['top'] + dic['height']))
    right_bottom = (int(dic['left'] + dic['width']), int(dic['top'] + dic['height']))
    right_top = (int(dic['left'] + dic['width']), int(dic['top']))
    cv2.line(img, left_top, left_bottom, color, 2)
    cv2.line(img, left_top, right_top, color, 2)
    cv2.line(img, right_bottom, left_bottom, color, 2)
    cv2.line(img, right_bottom, right_top, color, 2)

    cv2.putText(img, text, (int(dic['left']), int(dic['top']) + 20), cv2.FONT_HERSHEY_COMPLEX, 1, color, 1)


class BaiduAIP(object):
    def __init__(self):
        self.client = AipBodyAnalysis(cfg.APP_ID, cfg.API_KEY, cfg.SECRET_KEY)

    def bodyAnalysis(self, img_jpg):
        etval, buffer = cv2.imencode('.jpg', img_jpg)
        result = self.client.bodyAnalysis(buffer)  # 内部把buffer转换为base64了
        return result


if __name__ == '__main__':
    baiduapi = BaiduAIP()
    img = cv2.imread('./data/test.jpg')
    t1 = time.time()
    d = baiduapi.bodyAnalysis(img)
    t2 = time.time()
    print("api time= " + str(t2 - t1))
    print(d["person_num"])
    print(d["log_id"])
    persion = d["person_info"]
    for p in persion:
        draw_line(img, p['body_parts'], 'ok')
        draw_point(img, p['body_parts'], 'ok')
        draw_box(img, p['location'], 'beauty')
    t3 = time.time()
    print("draw time= " + str(t3 - t2))
    cv2.imwrite("./data/test_ok.jpg", img)