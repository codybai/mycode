def save_to_pkl():
    file_image = "file_image/"
    file_text = "file_text/"
    f1= open("dataset.pkl","wb+")
    num_data = 4
    total = []
    for i in range(num_data):  #4为数据的个数
        image_path = file_image+str(i)+".jpg"
        text_path = file_text+str(i)+".txt"
        image = np.array(Image.open(image_path))
        f = open(text_path)
        label = f.readline().strip()
        f.close()
        total.append([image,label])
        print("已经拼接:%d/%d" % (i+1 , num_data))
    # print(total)
    try:
        pkl.dump(total,f1)
    except:
        print("保存失败！")
    f1.close()
    print("保存成功！")