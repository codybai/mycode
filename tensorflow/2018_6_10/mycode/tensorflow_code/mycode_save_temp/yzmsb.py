from captcha.image import ImageCaptcha
import numpy as np
from PIL import Image
import random
import sys

number=['0','1','2','3','4','5','6','7','8','9',]

def random_captcha_text(char_set = number,captcha_size = 4):
    captcha_text=[]
    for i in range(captcha_size):
        c = random.choice(char_set)
        captcha_text.append(c)
    return captcha_text

def get_captcha_text_and_image():
    image = ImageCaptcha()

    captcha_text =  random_captcha_text()
    #验证码转为字符串
    captcha_text = ''.join(captcha_text)

    #生成验证码
    captcha = image.generate(captcha_text)

    #baocun
    image.write(captcha_text,'yzmimage/'+captcha_text+'.jpg')

#数量少于10000，因为重名
num=10000
if __name__ =='__main__':
    for i in range(num):
        get_captcha_text_and_image()
        sys.stdout.write('\r>>Creating image %d/%d' %(i+1,num))
        sys.stdout.flush()
    sys.stdout.write('\n')
    sys.stdout.flush()

    print('生成完毕')