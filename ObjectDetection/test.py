# import cv2
#
# img = r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\MachineLearning\pos\Pontos_Buffer_51.jpg'
# img = cv2.imread(img)
# while True:
#     size = img.shape
#     val = 75
#     print(val, val, size[0]-val, size[1]-val)
#     cv2.rectangle(img, (val, val), (size[0]-val, size[1]-val), (0, 255, 0), 2)
#     cv2.imshow("img", img)
#     key = cv2.waitKey(1)
#     if key == 27:
#         break
#
# cv2.destroyAllWindows()

#=================================================================================================================
#
# import os
# import glob
#
# Pasta = r"E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\MachineLearning\pos"
#
# with open(Pasta + r"\pos.info", "w+") as file:
#     imgs = glob.glob(Pasta + "\*.jpg")
#     for img in imgs:
#         text = "{0} 1 0 0 50 50\n".format(img)
#         file.write(text)

#=================================================================================================================


# from PIL import Image
# import glob
#
# Pasta = r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\MachineLearning\pos'
#
# files = glob.glob(Pasta + "\*.jpg")
# for file in files:
#     im = Image.open(file)
#     im = im.crop((75, 75, 125, 125))
#     im.save(file)

from PIL import Image
import os, sys

path = r"E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\MachineLearning\p"
dirs = os.listdir(path)

def resize():
    for item in dirs:
        print(item)
        if os.path.isfile(path + "\\" + item):
            im = Image.open(path + "\\" + item)
            f, e = os.path.splitext(path + "\\" + item)
            imResize = im.resize((24, 24), Image.ANTIALIAS)
            imResize.save(path + "\\" + item, 'JPEG', quality=90)

resize()