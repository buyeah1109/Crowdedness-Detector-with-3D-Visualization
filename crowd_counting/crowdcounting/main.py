from application.crowdedness import CrowdednessDetector
from application.application import CrowdCounter
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import os
import time

# Test crowdness.py

# t = time.time()
# os.environ['KMP_DUPLICATE_LIB_OK']='True'
#
# img_path = 'data/images/2.jpg'
# pil_im = Image.open(img_path)
# with open(img_path, 'rb') as image:
#     b = image.read()
# detector = CrowdednessDetector(b, _radius = 100, _area = 100)
#
# cnt, density_map = detector.count_density_map()
# cr = detector.get_crowdedness(density_map)
# print(cnt, cr)
# print("done, used {} time.".format(round(time.time() - t)))
# imshow(density_map)
# plt.show()

t = time.time()
os.environ['KMP_DUPLICATE_LIB_OK']='True'
img_path = 'data/images/2.jpg'
gpu_id = -1
mcnn_path = 'data/models/mcnn_shtechA_660.h5'
with open(img_path, 'rb') as image:
     b = image.read()
detector = CrowdednessDetector(_radius = 100, _area = 100)
counter = CrowdCounter(_mcnnmodelpath=mcnn_path, _gpuID= gpu_id)

cnt_detector, density_map = detector.count_density_map(b)
cr = detector.get_crowdedness(density_map)
cnt_dual = counter.count(b)
print("Dual Model Prediction: {}, Single Pred: {}, Crowdedness: {}".format(cnt_dual, cnt_detector, cr))
print("Done, used {} time.".format(round(time.time() - t)))
# imshow(density_map)
# plt.show()