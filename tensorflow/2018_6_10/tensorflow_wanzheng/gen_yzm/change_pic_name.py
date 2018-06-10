from PIL import Image
import os
root = 'C:/Users/baicol/Desktop/tianchi/part2/'

def merge_image(dir):
    for filename in os.listdir(root+dir):
        img = Image.open(root+dir+"/"+filename)
        print(root+dir+"/"+filename)
        img.save('C:/Users/baicol/Desktop/tianchi/part2/all_image/' + dir+filename, format="png")

for i in range(1,5):
    merge_image("genyzm_"+str(i))
