from application.crowdedness import CrowdednessDetector
from application.application import CrowdCounter
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
import os
import numpy as np
import time
from application.picture_lib import fetch, getCount, getCrowdness

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


os.environ['KMP_DUPLICATE_LIB_OK']='True'
gpu_id = -1
mcnn_path = 'data/models/mcnn_shtechA_660.h5'
detector = CrowdednessDetector(_radius = 100, _area = 100)
counter = CrowdCounter(_mcnnmodelpath=mcnn_path, _gpuID= gpu_id)

picpath = fetch('festivalwalk', '6', '2')
pic_info = np.load(picpath, allow_pickle=True)
img_path = pic_info.item().get('path')

t = time.time()
with open(img_path, 'rb') as image:
     b = image.read()
cnt_detector, density_map = detector.count_density_map(b)
cnt_dual = counter.count(b)
cr = detector.get_crowdedness(density_map, cnt_dual)

pic_info.item()['cnt'] = cnt_dual
pic_info.item()['cr'] = cr
np.save(picpath, pic_info.item())

print(pic_info.item().get('path'))
print("Dual Model Prediction: {}, Single Pred: {}, Crowdedness: {}".format(cnt_dual, cnt_detector, cr))
print("Done, used {} time.".format(round(time.time() - t)))


# imshow(density_map)
# plt.show()
