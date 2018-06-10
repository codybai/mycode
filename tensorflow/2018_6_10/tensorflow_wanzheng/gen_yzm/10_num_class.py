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
filePath = "C:/Users/baicol/Desktop/tianchi/part2/label/"
def genDict():
	dic = []
	for filename in os.listdir(filePath):
		if not filename.startswith("."):
			with open(filePath + filename, encoding='utf-8') as file:
				for line in file.readlines():
					content = line.split(",")[8]
					if "###" not in content:
						for c in content:
							if c != '\n':
								dic.append(c)
	# for c in [chr(x) for x in range(33,127)]:
	# 	dic.append(c)
	d = list(set(dic))
	with open("h_dictset.txt",'w+', encoding='utf-8') as out:
		for c in d:
			out.write(c + '\n')
	return d


def gen_one_yzm(char1,filename):
        with open('C:/Users/baicol/Desktop/tianchi/part2/mylabel/'+filename+".txt","w+",encoding='utf-8') as file:
            for c in char1:
                file.write(c)
        print(char1)
        str_len=len(char1)
        print('char1len',str_len)
        print('filename',filename)
        charlen = 256
        if str_len*32>charlen:
                charlen=str_len*30

        # img1 = Image.new(mode="RGB", size=(charlen, 32), color=(int(random.uniform(0,255)/2),int(random.uniform(0,255)/3),int(random.uniform(0,255)/4)))#随机底色
        img1 = Image.new(mode="RGB", size=(charlen, 32), color=(255,255,255)) #白底
        draw1 = ImageDraw.Draw(img1, mode="RGB")

        # 每循环一次重新生成随机颜色
        color1 = (0, 0,0)

        # 把生成的字母或数字添加到图片上
        # 图片长度为120px,要生成5个数字或字母则每添加一个,其位置就要向后移动24px
        # font1 = ImageFont.truetype("simhei.ttf", 32)#黑体
        font1 = ImageFont.truetype("simfang.ttf", 32)#仿宋体

        draw1.text([1, 0], char1, color1, font=font1)
        img1=img1.resize((256, 32))
        # 把生成的图片保存为"pic.png"格式
        img1.save('C:/Users/baicol/Desktop/tianchi/part2/myimage/'+filename+".png", format="png")
filepath='C:/Users/baicol/Desktop/tianchi/part2/itext/'
# d = genDict()[:100]
d = "坡、中国中国较上创新领域创新驱动战略，在科研和教育投入等方面保持高强度，但受外部市场变化，高科技制成品出口有所下降，拖累该项竞争力排名，位列第8位博鳌亚洲论坛2018年年会新闻发布会暨旗舰报告发布会在博鳌亚洲论坛新闻中心举行，会上发布了《亚洲经济一体化报告》、《新兴经济体报告》、《亚洲竞争力报告》三大学术报告。此次发布的《亚"

d = list(set(d))
print(len(d))
print(d)
print('start')
filename = ''
for i in range(10000):
    text = ''
    len = random.uniform(5,18)
    for i in range(0,int(len)):
        index = random.uniform(0, 100)
        text+=d[int(index)]
    gen_one_yzm(text, str(i))


