
import imghdr
from unicodedata import name
import cv2 as cv
import numpy as np
#
print("欢迎使用本模块，本模块的功能很简单，可以让自己更好的操作opencv模块的功能");
def ImgRead(img,i,name,waitkey):
    imgshowimg=cv.imread(img,i);
    rs=cv.imshow(name,imgshowimg);
    cv.waitKey(waitkey);
    cv.destroyAllWindows();