from flask import request, make_response, Flask
import os
import json
import socket
import sys
import predicting_model.predict as pr

os.system('')
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
insertList = os.listdir(os.path.dirname(__file__) + "\\static")
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)


@app.route('/imageList/<name>', methods=['GET'])
def imageList(name):
    if name not in insertList:
        return None
    else:
        path = os.path.dirname(__file__) + "\\static\\" + name
        imgList = os.listdir(path)
        returnJson = dict()
        returnJson["length"] = len(imgList)
        imgPathList = [(str(ip) + "/static/" + name + "/" + i)
                       for i in imgList]
        returnJson["paths"] = imgPathList
        return returnJson


@app.route('/predict', methods=['POST','GET'])
def upload():
    theFile = request.files.get('file')
    # print(theFile.filename, file=sys.stderr)
    # print(type(theFile), file=sys.stderr)
    theName = theFile.filename
    # if theFile is None:
    #     return "Error, none has been upload"
    imgPath = os.path.dirname(__file__) + "\\storeImg\\" + theName

    theFile.save(imgPath)

    specie = pr.predict(imgPath,2,True)

    return (specie)


# if __name__ == '__main__':
#     app.run(debug=True,host='1.2.3.4',port=1231)