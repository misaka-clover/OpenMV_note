# Automatic Grayscale Color Tracking Example
# 自动灰度颜色追踪例程
#
# This example shows off single color automatic grayscale color tracking using the OpenMV Cam.
# 这个例子展示了使用OpenMV的单色自动灰度色彩跟踪。

import sensor, image, time
print("Letting auto algorithms run. Don't put anything in front of the camera!")

sensor.reset()
sensor.set_pixformat(sensor.GRAYSCALE)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

# Capture the color thresholds for whatever was in the center of the image.
# 捕捉图像中心的颜色阈值。
r = [(320//2)-(50//2), (240//2)-(50//2), 50, 50] # 50x50 center of QVGA.

print("Auto algorithms done. Hold the object you want to track in front of the camera in the box.")
print("MAKE SURE THE COLOR OF THE OBJECT YOU WANT TO TRACK IS FULLY ENCLOSED BY THE BOX!")
for i in range(60):
    img = sensor.snapshot()
    img.draw_rectangle(r)
    print("i1 =", i)

print("Learning thresholds...")
threshold = [128, 128] # Middle grayscale values.
                        # 中间灰度值
                        # 由于是灰度，所以LAB中只需要L就行，min and max L
                        # 不过建议手动确定阈值为佳
for i in range(60):
    img = sensor.snapshot()
    print("i2 =", i)

    # 在 roi 的所有颜色通道上进行标准化直方图运算，并返回 histogram 对象。
    hist = img.get_histogram(roi=r)
    lo = hist.get_percentile(0.1) # Get the CDF of the histogram at the 1% range (ADJUST AS NECESSARY)!
                                    # 获取1％范围的直方图的CDF（根据需要调整）！
    hi = hist.get_percentile(0.9) # Get the CDF of the histogram at the 99% range (ADJUST AS NECESSARY)!
                                    # 获取99％范围的直方图的CDF（根据需要调整）！
    
    # Average in percentile values.
    # 平均百分位值。
    threshold[0] = (threshold[0] + lo.value()) // 2
    threshold[1] = (threshold[1] + hi.value()) // 2
    for blob in img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, merge=True, margin=10):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        img.draw_rectangle(r)

print("Thresholds learned...")
print("Tracking colors...")

while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs([threshold], pixels_threshold=100, area_threshold=100, merge=True, margin=10):
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
    print("threshold =", threshold, "FPS =", clock.fps())





