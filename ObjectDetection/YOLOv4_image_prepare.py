import cv2
import os

Pasta = r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\YOLOV4\images'
files = os.listdir(Pasta)
text = "0 0.488281 0.511719 0.195312 0.195312"
for f in files:
    if f.endswith(".jpg"):
        caminho = os.path.join(Pasta, f)
        nome = f[:-4]
        with open("{0}/{1}.txt".format(Pasta, nome), "w+") as txt:
            txt.write(text)
print("Concluído")