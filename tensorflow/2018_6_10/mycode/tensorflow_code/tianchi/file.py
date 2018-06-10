import os
import math
from PIL import Image
def readfile():
    filepath   = "./txt/"
    imagepath  = "./image/"
    resultpath = "./iphoto/"
    labelpath = "./itext/"
    i = 0
    for filename in os.listdir(filepath):
        if not filename.startswith("."):
            imagename = os.path.splitext(filename)[0] +".jpg"
            print(imagename)
            with open(filepath + filename, encoding='utf-8') as file:
                with Image.open(imagepath + imagename) as image:
                    for line in file.readlines():
                        split = line.split(",")
                        content = split[8]
                        if "###" not in content:
                            im = image.copy()
                            w, h = im.size
                            centerX, centerY = w/2.0, h/2.0
                            startX, startY, endX, endY, dy, dx = sortCoord(split)
                            if dx != 0:
                                theta = math.atan(dy / dx)
                                #print(startX,startY,endX,endY,dy,dx)
                                if math.fabs(theta) > 0.1745329: #10度以上调整
                                    if theta < 0:  #顺时针
                                        x0, y0 = startX, startY
                                        startX = (x0 - centerX) * math.cos(2* math.pi - theta) - (y0 - centerY) * math.sin(2* math.pi - theta) + centerX
                                        startY = (x0 - centerX) * math.sin(2* math.pi - theta) + (y0 - centerY) * math.cos(2* math.pi - theta) + centerY
                                        x0, y0 = endX, endY
                                        endX = (x0 - centerX) * math.cos(2* math.pi - theta) - (y0 - centerY) * math.sin(2* math.pi - theta) + centerX
                                        endY = (x0 - centerX) * math.sin(2* math.pi - theta) + (y0 - centerY) * math.cos(2* math.pi - theta) + centerY
                                    else:          #逆时针
                                        x0, y0 = startX, startY
                                        startX = (x0 - centerX) * math.cos(theta) - (y0 - centerY) * math.sin(theta) + centerX
                                        startY = (x0 - centerX) * math.sin(theta) + (y0 - centerY) * math.cos(theta) + centerY
                                        x0, y0 = endX, endY
                                        endX = (x0 - centerX) * math.cos(theta) - (y0 - centerY) * math.sin(theta) + centerX
                                        endY = (x0 - centerX) * math.sin(theta) + (y0 - centerY) * math.cos(theta) + centerY
                                    #弧度变角度
                                    theta = theta * 180 / math.pi
                                    im = im.rotate(theta, expand = True)
                            w, h = im.size
                            centerXR, centerYR = w/2.0, h/2.0
                            startX += (centerXR - centerX)
                            startY += (centerYR - centerY)
                            endX += (centerXR - centerX)
                            endY += (centerYR - centerY)
                            endX = endX if endX < w else w
                            endY = endY if endY < h else h
                            box = (startX, startY, endX, endY)
                            imc = im.crop(box)
                            imc = imc.resize((192, 32), Image.ANTIALIAS)
                            imc = imc.convert("RGB")
                            imc.save(resultpath + str(i) + ".jpg")
                            with open(labelpath + str(i) + ".txt", 'w', encoding = 'utf-8') as file:
                                file.write(content)
                            print("%s %f",(filename, i))
                            i += 1
def sortCoord(line):
    x = [float(line[z]) for z in [0,2,4,6]]
    y = [float(line[z]) for z in [1,3,5,7]]
    L = list(zip(x,y))
    l1 = sorted(L, key = lambda z:z[0])
    l2 = [l1[z] for z in [0,1]]
    l3 = [l1[z] for z in [2,3]]
    l4 = sorted(l2, key = lambda z:z[1])
    l5 = sorted(l3, key = lambda z:z[1])
    l6 = l4 + l5
    #print(l6)
    return l6[0][0],l6[0][1],l6[3][0],l6[3][1],l6[2][1]-l6[0][1],l6[2][0]-l6[0][0]
readfile()
