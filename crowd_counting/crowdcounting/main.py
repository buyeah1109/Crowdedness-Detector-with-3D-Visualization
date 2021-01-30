from application.crowdedness import CrowdednessDetector
from PIL import Image
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import os
import time

t = time.time()
os.environ['KMP_DUPLICATE_LIB_OK']='True'

img_path = 'data/images/2.jpg'
pil_im = Image.open(img_path)
with open(img_path, 'rb') as image:
    b = image.read()
detector = CrowdednessDetector(b, _radius = 100, _area = 100)

cnt, density_map = detector.count_density_map()
cr = detector.get_crowdedness(density_map)
print(cnt, cr)
print("done, used {} time.".format(round(time.time() - t)))
imshow(density_map)
plt.show()