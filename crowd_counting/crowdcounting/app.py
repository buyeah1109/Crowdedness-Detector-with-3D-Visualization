from flask import Flask, render_template, request, send_from_directory
from flask_bootstrap import Bootstrap
import json
app = Flask(__name__)
bootstrap = Bootstrap(app)

@app.route('/')
def index():
    title = 'Flask web app'
    return render_template('index.html', title=title)


@app.route('/file/cv', methods=["GET"])
def file():
    response = send_from_directory(directory='file', filename='cv.png')
    return response


@app.route('/data')
def data():
    # here we want to get the value of user (i.e. ?user=some-value)
    query = request.query_string
    s = query.decode("utf-8")

    floor = request.args.get('floor')
    mall = request.args.get('mall')
    section = request.args.get('section')

    
    return 0


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)


