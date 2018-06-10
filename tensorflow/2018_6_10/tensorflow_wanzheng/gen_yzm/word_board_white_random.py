#!/usr/bin/python
# -*- coding: UTF-8 -*-
# 导入random模块
import random
import  os
# 导入Image,ImageDraw,ImageFont模块
from PIL import Image, ImageDraw, ImageFont

# 定义使用Image类实例化一个长为120px,宽为30px,基于RGB的(255,255,255)颜色的图片

#照片可以自己定
# 实例化一支画笔


# 定义要使用的字体

def gen_one_yzm(char1,filename):
        str_len=len(char1)
        print('char1len',str_len)
        print('filename',filename)
        charlen = 256
        if str_len*32>charlen:
                charlen=str_len*30

        img1 = Image.new(mode="RGB", size=(charlen, 32), color=(int(random.uniform(0,255)/2),int(random.uniform(0,255)/3),int(random.uniform(0,255)/4)))#随机底色
        draw1 = ImageDraw.Draw(img1, mode="RGB")

        # 每循环一次重新生成随机颜色
        color1 = (255, 255,255)

        # 把生成的字母或数字添加到图片上
        # 图片长度为120px,要生成5个数字或字母则每添加一个,其位置就要向后移动24px
        font1 = ImageFont.truetype("simhei.ttf", 32)#黑体


        draw1.text([1, 0], char1, color1, font=font1)
        img1=img1.resize((256, 32))
        # 把生成的图片保存为"pic.png"格式
        img1.save('C:/Users/baicol/Desktop/tianchi/part2/genyzm/'+filename+".png", format="png")
filepath='C:/Users/baicol/Desktop/tianchi/part2/itext/'
for filename in os.listdir(filepath):
        # print(filename)
        s = filepath+filename
        with open(s,encoding='utf-8') as file:
                for i in file:
                        gen_one_yzm(i,filename.split('.')[0])

