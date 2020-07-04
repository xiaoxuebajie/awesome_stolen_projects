import sys
import cv2
import tkinter as tk
from tkinter import *  # 文件控件
from PIL import Image, ImageTk  # 图像控件
import threading  # 多线程
from aip_bodyanalysis import *
import time

IMG_HEIGT = 352 * 2
IMG_WIDTH = 640 * 2

aip = BaiduAIP()
is_run = True

# 申请线程锁
lock = threading.Lock()

# 根窗口
window = tk.Tk()

# 显示变量
num_people = StringVar()
num_people.set('当前人数：0')
num_desertion = StringVar()
num_desertion.set('不正常：0')

# UI绘制
window.title("测试")
sw = window.winfo_screenwidth()  # 获取屏幕宽
sh = window.winfo_screenheight()  # 获取屏幕高

# 设置窗口大小和位置
wx = IMG_WIDTH + 100
wh = IMG_HEIGT + 100
window.geometry("%dx%d+%d+%d" % (wx, wh, (sw - wx) / 2, (sh - wh) / 2 - 100))  # 窗口至指定位置

# 顶部是信息栏
fm1 = Frame(window)
Label(fm1, text="总人数：20").pack(side='left')
label_num = Label(fm1, textvariable=num_people).pack(side='left')
label_num = Label(fm1, textvariable=num_desertion).pack(side='left')
fm1.pack(side='top', padx=10)

# 左侧是操作栏
fm2 = Frame(window)
fm2.pack(side='left', padx=10)
canvas1 = tk.Canvas(window, bg="#c4c2c2", height=IMG_HEIGT, width=IMG_WIDTH)  # 绘制画布
canvas1.pack(side="left")


def getResult(img):
    d = aip.bodyAnalysis(img)
    if ("person_info" not in d):
        return
    persion = d["person_info"]
    # 获取人数
    num = len(persion)
    num_people.set("当前人数：" + str(num))
    # 绘制人体姿势
    for p in persion:
        status = pose_analyse(img, p['body_parts'])
        draw_line(img, p['body_parts'], status)
        draw_point(img, p['body_parts'], status)
        draw_box(img, p['location'], status)


def cc():
    capture = cv2.VideoCapture('./data/awesome.mp4')
    # capture = cv2.VideoCapture(0)
    while capture.isOpened():
        t0 = time.time()
        _, frame = capture.read()
        # 清除缓存
        for i in range(15):
            _, frame = capture.read()
        getResult(frame)
        frame = cv2.flip(frame, 1)  # 翻转 0:上下颠倒 大于0水平颠倒
        cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
        img = Image.fromarray(cv2image)
        image_file = ImageTk.PhotoImage(img)
        canvas1.create_image(0, 0, anchor="nw", image=image_file)
        print(time.time() - t0)
    print("ending")


class ImgProcThread(threading.Thread):
    def __init__(self, *args, **kwargs):
        super(ImgProcThread, self).__init__(*args, **kwargs)
        self.__flag = threading.Event()  # 用于暂停线程的标识
        self.__flag.set()  # 设置为True
        self.__running = threading.Event()  # 用于停止线程的标识
        self.__running.set()  # 将running设置为True

    def run(self):
        capture = cv2.VideoCapture('./data/awesome.mp4')
        while self.__running.isSet() and capture.isOpened():
            self.__flag.wait()  # 为True时立即返回, 为False时阻塞直到内部的标识位为True后返回
            t0 = time.time()
            _, frame = capture.read()
            for i in range(15):
                _, frame = capture.read()
            frame = cv2.resize(frame, (IMG_WIDTH, IMG_HEIGT), interpolation=cv2.INTER_NEAREST)
            getResult(frame)
            # frame = cv2.flip(frame, 1)#翻转 0:上下颠倒 大于0水平颠倒
            cv2image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGBA)
            img = Image.fromarray(cv2image)
            image_file = ImageTk.PhotoImage(img)
            canvas1.create_image(0, 0, anchor="nw", image=image_file)
            print(time.time() - t0)

    def pause(self):
        self.__flag.clear()  # 设置为False, 让线程阻塞

    def resume(self):
        self.__flag.set()  # 设置为True, 让线程停止阻塞

    def stop(self):
        self.__flag.set()  # 将线程从暂停状态恢复, 如何已经暂停的话
        self.__running.clear()  # 设置为Fals


def video_demo():
    t = threading.Thread(target=cc)
    t.start()


job = ImgProcThread()

bt_start = tk.Button(fm2, text="启动", height=2, width=15, command=job.start).pack(side="top")
bt_pause = tk.Button(fm2, text="暂停", height=2, width=15, command=job.pause).pack(side="top")
bt_resume = tk.Button(fm2, text="恢复", height=2, width=15, command=job.resume).pack(side="top")
bt_stop = tk.Button(fm2, text="结束线程", height=2, width=15, command=job.stop).pack(side="top")
bt_quit = tk.Button(fm2, text="退出程序", height=2, width=15, command=window.quit).pack(side="top")

window.mainloop()