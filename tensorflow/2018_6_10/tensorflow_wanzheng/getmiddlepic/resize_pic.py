from PIL import Image
import os
# from_image='C:/BaiduyunDownLoad/猫狗大战数据集/train_original/train'
# to_image='C:/BaiduyunDownLoad/猫狗大战数据集/train/'
from_image='C:/BaiduyunDownLoad/猫狗大战数据集/test1_original/test1'
to_image='C:/BaiduyunDownLoad/猫狗大战数据集/test1/'
for filename in os.listdir(from_image):
    path = os.path.join(from_image,filename)
    print(path)
    img = Image.open(path)
    img = img.resize((256,256))
    img.save( to_image+ filename)
