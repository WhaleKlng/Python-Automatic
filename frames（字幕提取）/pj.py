import os
from PIL import Image

high_size = 144#高
width_size = 1280#宽

path = '.\\图片缓存\\'
imghigh = sum([len(x) for _, _, x in os.walk(os.path.dirname(path))])#获取当前文件路径下的文件个数
print(imghigh)
imagefile = []
for root,dirs,files in os.walk(path):
    for f in files:
        imagefile.append(Image.open(path+f))

target = Image.new('RGB',(width_size,high_size*imghigh))#最终拼接的图像的大小
left = 0
right = high_size
for image in imagefile:
    target.paste(image,(0,left,width_size,right))
    left += high_size#从上往下拼接，左上角的纵坐标递增
    right += high_size#左下角的纵坐标也递增
    target.save(path+'result.jpg',quality=100)