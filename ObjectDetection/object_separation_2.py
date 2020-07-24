# import the necessary packages
import numpy as np
import imutils
import cv2
import PySimpleGUI as sg
import os

IMG = r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\Treino\b.jpg'

def nothing(x):
	pass

cv2.namedWindow("Trackbars")
cv2.namedWindow("Params")

cv2.createTrackbar("L-H", "Trackbars", 16, 179, nothing)
cv2.createTrackbar("L-S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 229, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("param0", "Params", 50, 50, nothing)
cv2.createTrackbar("param1", "Params", 300, 300, nothing)
cv2.createTrackbar("param2", "Params", 7, 50, nothing)
cv2.createTrackbar("MinRadius", "Params", 1, 100, nothing)
cv2.createTrackbar("MaxRadius", "Params", 1, 100, nothing)
cv2.createTrackbar("LineSize", "Params", 20, 100, nothing)

while True:
	image = cv2.imread(IMG)
	out = image.copy()
	hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
	l_h = cv2.getTrackbarPos("L-H", "Trackbars")
	l_s = cv2.getTrackbarPos("L-S", "Trackbars")
	l_v = cv2.getTrackbarPos("L-V", "Trackbars")
	u_h = cv2.getTrackbarPos("U-H", "Trackbars")
	u_s = cv2.getTrackbarPos("U-S", "Trackbars")
	u_v = cv2.getTrackbarPos("U-V", "Trackbars")
	lower_blue = np.array([l_h, l_s, l_v])
	upper_blue = np.array([u_h, u_s, u_v])
	mask = cv2.inRange(hsv, lower_blue, upper_blue)
	result = cv2.bitwise_and(image, image, mask=mask)

	#resultgray = cv2.cvtColor(mask, cv2.COLOR_HLS2BGR)
	resultgray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
	resultgray = cv2.GaussianBlur(resultgray, (5, 5), cv2.BORDER_DEFAULT)
	param0 = cv2.getTrackbarPos("param0", "Params")
	param1 = cv2.getTrackbarPos("param1", "Params")
	param2 = cv2.getTrackbarPos("param2", "Params")
	minradius = cv2.getTrackbarPos("MinRadius", "Params")
	maxradius = cv2.getTrackbarPos("MaxRadius", "Params")
	Linesize = cv2.getTrackbarPos("LineSize", "Params")
	circles = cv2.HoughCircles(resultgray, cv2.HOUGH_GRADIENT, 0.9, param0, param1=param1, param2=param2, minRadius=minradius, maxRadius=maxradius)
	try:
		circles = np.uint16(np.around(circles))
		for (x, y, r) in circles[0, :]:
			cv2.circle(out, (x, y), r+Linesize, (0, 255, 0), 3)
	except TypeError:
		pass

	cv2.imshow("frame", image)
	cv2.imshow("mask", mask)
	cv2.imshow("result", result)
	cv2.imshow("circles", out)
	key = cv2.waitKey(1)
	if key == 27:
		break
	if key == 115:
		caminho = sg.popup_get_file("Salvar arquivo em:", no_window=True, save_as=True, file_types=(('Imagem', '*.tif *.png *.jpg'),))
		if caminho is not None:
			if caminho.endswith(".tif") or caminho.endswith(".TIF") or caminho.endswith(".png") or caminho.endswith(".PNG") or caminho.endswith(".jpg") or caminho.endswith(".JPG"):
				if not os.path.isfile(caminho):
					cv2.imwrite(caminho, out)
				else:
					sg.PopupOK("Arquivo já existe.")
			else:
				sg.PopupOK("Extensão inválida.")

cv2.destroyAllWindows()
# cv2.imwrite(r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\Imagem\Antenas.tif', out)
# print("Concluído")