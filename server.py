from flask import request, make_response, Flask
import os
import json
import socket
import sys
import predicting_model.predict as pr
from database.database import db, Insert

os.system('')
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False

baseDir = os.path.abspath(os.path.dirname(__file__)) + "/database"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    baseDir, 'inserts.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

insertList = os.listdir(os.path.dirname(__file__) + "/static")
# hostname = socket.gethostname()
# ip = socket.gethostbyname(hostname)


@app.route('/imageList/<name>', methods=['GET'])
def imageList(name):
    if name not in insertList:
        return None
    else:
        path = os.path.dirname(__file__) + "/static/" + name
        imgList = os.listdir(path)
        returnJson = dict()
        returnJson["length"] = len(imgList)
        imgPathList = [("static/" + name + "/" + i) for i in imgList]
        returnJson["paths"] = imgPathList
        return returnJson


@app.route('/predict', methods=['POST'])
def predict():

    theFile = request.files.get('file')
    theName = theFile.filename
    imgPath = os.path.dirname(__file__) + "/storeImg/" + theName
    theFile.save(imgPath)
    specie = pr.predict(imgPath, 2, False)
    specieJson = Insert.query.filter_by(
        latin_name="micromelalopha troglodyta").first().to_json()
    return specieJson.replace("\'", "\"")


@app.route('/all', methods=['GET'])
def all():
    inserts = Insert.query.all()
    insertJsonList = []
    for i in inserts:
        i = i.to_json()
        insertJsonList.append(i)
    return str(insertJsonList).replace("\'", "\"")


# if __name__ == '__main__':
#     app.run(host='0.0.0.0')