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

picpath = fetch('festivalwalk', '3', '1')
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


from flask import Flask, render_template, request, send_from_directory
from flask_bootstrap import Bootstrap
from crowd_counting.crowdcounting.application.picture_lib import getCount, getCrowdness

import json
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    title = 'Flask web app'
    return render_template('index.html', title=title)


@app.route('/cv', methods=["GET"])
def cv():
    response = send_from_directory(directory='file', filename='cv.png')
    return response

@app.route('/people', methods=["GET"])
def people():
    response = send_from_directory(directory='file', filename='people.png')
    return response

@app.route('/crowd', methods=["GET"])
def crowd():
    response = send_from_directory(directory='file', filename='crowd.png')
    return response

@app.route('/algorithm', methods=["GET"])
def algorithm():
    response = send_from_directory(directory='file', filename='algorithm.png')
    return response

@app.route('/xdd', methods=["GET"])
def xdd():
    response = send_from_directory(directory='file', filename='xdd.jpeg')
    return response

@app.route('/gzf', methods=["GET"])
def gzf():
    response = send_from_directory(directory='file', filename='gzf.jpeg')
    return response

@app.route('/zjw', methods=["GET"])
def zjw():
    response = send_from_directory(directory='file', filename='zjw.jpeg')
    return response

@app.route('/zmj', methods=["GET"])
def zmj():
    response = send_from_directory(directory='file', filename='zmj.jpeg')
    return response


@app.route('/data')
def data():
    # here we want to get the value of user (i.e. ?user=some-value)
    query = request.query_string
    s = query.decode("utf-8")

    floor = request.args.get('floor')
    mall = request.args.get('mall')
    section = request.args.get('section')

    count = getCount(mall, floor, section)
    crowdedness = getCrowdness(mall, floor, section)

    return count +","+ crowdedness



if __name__ == '__main__':
    app.run(debug=True, host="127.0.0.1", port=8080)


