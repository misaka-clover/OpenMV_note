#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# By: Misaka_Clover

import sensor, image, time
import pyb
import math
from pyb import LED

red_led = LED(1)
green_led = LED(2)
blue_led = LED(3)

def Light():
    red_led.on()
    green_led.on()
    blue_led.on()

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.skip_frames(10)
sensor.set_auto_gain(False)                 # 这两项必须关闭
sensor.set_auto_whitebal(False)             # 那开启你们还有什么意思呢？……

clock = time.clock()

while(True):
    clock.tick()
    Light()
    img = sensor.snapshot().lens_corr(1.8)      # 拍照后进行畸变矫正
    # 使用霍夫变换在图像中查找圆，返回一个image.circle对象列表
    for c in img.find_circles(threshold=3500, x_margin=10, y_margin=10, r_margin=10,
                                r_min=2, r_max=100, r_step=2):
        area = (c.x()-c.r(), c.y()-c.r(), 2*c.r(), 2*c.r())
        # area为识别到的圆区域，即圆的外接矩形框
        statistics = img.get_statistics(roi=area)       # 像素颜色统计
        print(statistics)
        #(0,100,0,120,0,120)是红色的阈值，所以当区域内的众数（也就是最多的颜色），范围在这个阈值内，就说明是红色的圆。
        #l_mode()，a_mode()，b_mode()是L通道，A通道，B通道的众数。
        if 0 < statistics.l_mode() < 100 and 0 < statistics.a_mode() < 127 and 0 < statistics.b_mode() < 127:       # 如果圆是红色
            img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))           #识别到的红色圆形用红色的圆框出来
        else:
            img.draw_rectangle(area, color = (255, 255, 255))
            #将非红色的圆用白色的矩形框出来
    print("FPS %f" % clock.fps())








