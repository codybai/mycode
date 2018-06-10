from PIL import Image
import os
import os,shutil
root = 'C:/Users/baicol/Desktop/tianchi/part2/itext/'
dir1 = 'genyzm_1'
dir2 = 'genyzm_2'
dir3 = 'genyzm_3'
dir4 = 'genyzm_4'


def mycopyfile(srcfile,dstfile):
    if not os.path.isfile(srcfile):
        print("%s not exist!"%(srcfile))
    else:
        fpath,fname=os.path.split(dstfile)    #分离文件名和路径
        if not os.path.exists(fpath):
            os.makedirs(fpath)                #创建路径
        shutil.copyfile(srcfile,dstfile)      #复制文件
        print("copy %s -> %s"%( srcfile,dstfile))

def merge_image(dir):
    for filename in os.listdir(root):
        save_path ='C:/Users/baicol/Desktop/tianchi/part2/all_text/'+dir+filename
        mycopyfile('C:/Users/baicol/Desktop/tianchi/part2/itext/'+filename,save_path)

for i in range(1,5):
    merge_image("genyzm_"+str(i))
