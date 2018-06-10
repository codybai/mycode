# -*- coding: UTF-8 -*-
import os
from PIL import Image
import numpy as np
import pickle as pk
filePath = "./txt/"
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
	for c in [chr(x) for x in range(33,127)]:
		dic.append(c)
	d = list(set(dic))
	with open("h_dictset.txt",'w+', encoding='utf-8') as out:
		for c in d:
			out.write(c + '\n')
	return d

def save_to_pkl():
    file_image = "./iphoto/"
    file_text = "./itext/"
    f1= open("_dataset.pkl","wb")
    num_data = 15289
    total = []
    for i in range(num_data):  #4为数据的个数
        image_path = file_image+str(i)+".jpg"
        text_path = file_text+str(i)+".txt"
        image = Image.open(image_path)
        image = np.array()
        image = np.reshape(image,[32,256,3])
        print(np.shape(image))

        f = open(text_path,'r',encoding='utf-8')
        text = f.readline().strip()
        dic = genDict()
        label = [dic.index(x)+1 for x in text]
       # print(label)
      #  print(text)
        f.close()
        total.append([image,label])
        print("已经拼接:%d/%d" % (i+1 , num_data))
    # print(total)
    try:
        pk.dump(total, f1)
    except:
        print("保存错误！")
        f1.close()
        return
    f1.close()
    print("保存成功！")

save_to_pkl()


