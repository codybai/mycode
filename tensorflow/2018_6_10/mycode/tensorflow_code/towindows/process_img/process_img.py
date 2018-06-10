from PIL import Image
import numpy as np
import matplotlib.pyplot   as plt
from PIL import ImageFilter





# load a color image
im = Image.open("../iphoto/89.jpg")

# convert to grey level image
Lim = im.convert('L')
Lim.show()

# setup a converting table with constant threshold
threshold = 100
table = []
for i in range(256):
    if i < threshold:
        table.append(0)
    else:
        table.append(1)

# convert to binary image by the table
bim = Lim.point(table, '1')

bim.show()



'''
im = Image.open("../iphoto/12.jpg")

# 预定义的图像增强滤波器

im_contour = im.filter(ImageFilter.CONTOUR)#SMOOTH：平滑滤波

im_min = im.filter(ImageFilter.EDGE_ENHANCE_MORE)\
    .filter(ImageFilter.GaussianBlur(radius=0.5))\
    .filter(ImageFilter.EDGE_ENHANCE_MORE)\
    .filter(ImageFilter.GaussianBlur(radius=0.1))\

im.show()



.filter(ImageFilter.EDGE_ENHANCE)重要
• BLUR：模糊滤波

• CONTOUR：轮廓滤波

• DETAIL：细节滤波

• EDGE_ENHANCE：边界增强滤波

• EDGE_ENHANCE_MORE：边界增强滤波（程度更深）

• EMBOSS：浮雕滤波

• FIND_EDGES：寻找边界滤波

• SMOOTH：平滑滤波

• SMOOTH_MORE：平滑滤波（程度更深）

• SHARPEN：锐化滤波

• GaussianBlur(radius=2)：高斯模糊
'''