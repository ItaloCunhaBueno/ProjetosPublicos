# import the necessary packages
import numpy as np
import imutils
import cv2

IMG = r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\Treino\a.jpg'

def nothing(x):
	pass

cv2.namedWindow("Trackbars")

cv2.createTrackbar("L-H", "Trackbars", 20, 179, nothing)
cv2.createTrackbar("L-S", "Trackbars", 0, 255, nothing)
cv2.createTrackbar("L-V", "Trackbars", 229, 255, nothing)
cv2.createTrackbar("U-H", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-S", "Trackbars", 255, 255, nothing)
cv2.createTrackbar("U-V", "Trackbars", 255, 255, nothing)

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

	resultgray = cv2.cvtColor(result, cv2.COLOR_HLS2BGR)
	resultgray = cv2.cvtColor(result, cv2.COLOR_BGR2GRAY)
	resultgray = cv2.medianBlur(resultgray, 5)
	circles = cv2.HoughCircles(resultgray, cv2.HOUGH_GRADIENT, 1, 10, param1=200, param2=6, minRadius=0, maxRadius=6)
	try:
		circles = np.uint16(np.around(circles))
		for (x, y, r) in circles[0, :]:
			cv2.circle(out, (x, y), r+10, (0, 255, 0), 3)
	except TypeError:
		pass

	cv2.imshow("frame", image)
	cv2.imshow("mask", mask)
	cv2.imshow("result", result)
	cv2.imshow("circles", out)
	key = cv2.waitKey(1)
	if key == 27:
		break

cv2.destroyAllWindows()
# cv2.imwrite(r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\Imagem\Antenas.tif', out)
# print("Concluído")