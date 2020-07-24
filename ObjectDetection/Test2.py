import cv2
import matplotlib.pyplot as plt

# read images
img1 = cv2.imread(r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\MachineLearning\v1\Pontos_Buffer_3.jpg')
img2 = cv2.imread(r'E:\Trabalho\Projeto_Parabolicas\Teste_MachineLearning\MachineLearning\v1\test.jpg')

img4 = cv2.cvtColor(img2, cv2.COLOR_BGR2RGB)
Gimg1 = cv2.cvtColor(img1, cv2.COLOR_BGR2GRAY)
Gimg2 = cv2.cvtColor(img2, cv2.COLOR_BGR2GRAY)


sift = cv2.KAZE_create(threshold=0.001)

keypoints_1, descriptors_1 = sift.detectAndCompute(Gimg1, None)
keypoints_2, descriptors_2 = sift.detectAndCompute(Gimg2, None)

#feature matching
bf = cv2.BFMatcher(cv2.NORM_L1, crossCheck=True)

matches = bf.match(descriptors_1,descriptors_2)
matches = sorted(matches, key = lambda x:x.distance)

img3 = cv2.drawMatches(Gimg1, keypoints_1, img4, keypoints_2, matches, Gimg2, matchColor=(0, 255, 0), flags=2)
plt.imshow(img3),plt.show()