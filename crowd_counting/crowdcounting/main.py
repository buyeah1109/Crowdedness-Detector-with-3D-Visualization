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


