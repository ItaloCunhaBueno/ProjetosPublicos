# import the necessary packages
import numpy as np
import imutils
import cv2
import PySimpleGUI as sg
import os

IMG = r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\Imagem\BAIRRO_MANTIQUEIRA.tif'

image = cv2.imread(IMG)
out = image.copy()
hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
l_h = 30
l_s = 9
l_v = 237
u_h = 255
u_s = 255
u_v = 255
param0 = 50
param1 = 300
param2 = 1
minradius = 1
maxradius = 1
Linesize = 20

lower_blue = np.array([l_h, l_s, l_v])
upper_blue = np.array([u_h, u_s, u_v])
mask = cv2.inRange(hsv, lower_blue, upper_blue)
result = cv2.bitwise_and(image, image, mask=mask)

resultgray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
resultgray = cv2.GaussianBlur(resultgray, (5, 5), cv2.BORDER_DEFAULT)

circles = cv2.HoughCircles(resultgray, cv2.HOUGH_GRADIENT, 0.9, param0, param1=param1, param2=param2, minRadius=minradius, maxRadius=maxradius)
try:
	circles = np.uint16(np.around(circles))
	for (x, y, r) in circles[0, :]:
		cv2.circle(out, (x, y), r+Linesize, (0, 255, 0), 3)
except TypeError:
	pass

caminho = r"E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\Imagem\Mask2.tif"
cv2.imwrite(caminho, out)
cv2.destroyAllWindows()
print("Concluido")
# cv2.imwrite(r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\Imagem\Antenas.tif', out)
# print("Concluído")