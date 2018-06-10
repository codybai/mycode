from PIL import Image
import os
picfile='C:/Users/baicol/Desktop/tianchi/part2/genyzm_1'
pic_L='C:/Users/baicol/Desktop/tianchi/part2/genyzm_1_L/'
for filename in os.listdir(picfile):
    path = os.path.join(picfile,filename)
    image = Image.open(path).convert('L')
    image.save(pic_L + filename+ ".png")