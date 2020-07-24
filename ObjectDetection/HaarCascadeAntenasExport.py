import numpy as np
import cv2


model = r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\MachineLearning\V5_15stages_45Degree\cascade.xml'
sat_cascade = cv2.CascadeClassifier(model)

imgTest = r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\MachineLearning\Test\Test5_proc.tif'
img = cv2.imread(imgTest)
img2 = img.copy()
adjusted = cv2.convertScaleAbs(img, alpha=0, beta=0) #ajusta contraste
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print("Detectando features...")
sats = sat_cascade.detectMultiScale(gray, 1.05, 2, minSize=(29, 29), maxSize=(50, 50))
print("{0} features detectados.".format(len(sats)))
minval = 230
maxval = 255
lower = np.array([minval, minval, minval])
upper = np.array([maxval, maxval, maxval])
print("Analisando features...")
for (x,y,w,h) in sats:
    out = img[y:y+h, x:x+w]
    mask = cv2.inRange(out, lower, upper)
    HASWHITE = False
    for a in mask:
        if any(a)>0:
            HASWHITE = True
    if HASWHITE:
        cv2.rectangle(adjusted, (x, y), (x+w, y+h), (0, 255, 255), 2)
        cv2.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 255), 2)

print("Salvando Imagem...")
cv2.imwrite(r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\MachineLearning\Test\MaskV2.tif', adjusted)
print("Concluído")
# while True:
#     cv2.imshow("Antes", img)
#     cv2.imshow('Mascara', adjusted)
#     cv2.imshow("Resultado", img2)
#     k = cv2.waitKey(30) & 0xff
#     if k == 27:
#         break
#
# cv2.destroyAllWindows()
