import numpy as np
import cv2
import matplotlib.pyplot as plt


model = r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\MachineLearning\V5_15stages_45Degree\cascade.xml'
sat_cascade = cv2.CascadeClassifier(model)

imgTest = r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\MachineLearning\Test\test2.jpg'
img = cv2.imread(imgTest)
img2 = img.copy()
gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
print("Detectando features...")
sats = sat_cascade.detectMultiScale(gray, 1.05, 2, minSize=(29, 29), maxSize=(100, 100))
print("{0} features detectados.".format(len(sats)))
minval = 230
maxval = 255
lower = np.array([minval, minval, minval])
upper = np.array([maxval, maxval, maxval])
print("Analisando features...")
for (x, y, w, h) in sats:
    out = img[y:y+h, x:x+w]
    mask = cv2.inRange(out, lower, upper)
    HASWHITE = False
    for a in mask:
        if any(a) > 0:
            HASWHITE = True
    if HASWHITE:
        cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 255), 2)


# numpy_vertical_concat = np.concatenate((img, img2), axis=1)

# cv2.imshow("Resultado", numpy_vertical_concat)
# #cv2.imshow("Original", img2)
# cv2.waitKey(0)
# cv2.destroyAllWindows()
img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
img2 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)

columns = 2
rows = 1
fig = plt.figure(figsize=(8, 8))
plt.imshow(img2)
fig = plt.figure(figsize=(8, 8))
plt.imshow(img)
plt.show()