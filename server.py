from flask import request, make_response, Flask
import os
import json
import socket

os.system('')
app = Flask(__name__)
app.config["JSON_AS_ASCII"] = False
insertList = os.listdir(os.getcwd() + "\\static")
hostname = socket.gethostname()
ip = socket.gethostbyname(hostname)


@app.route('/imageList/<name>', methods=['GET'])
def imageList(name):
    if name not in insertList:
        return None
    else:
        path = os.getcwd() + "\\static\\" + name
        imgList = os.listdir(path)
        returnJson = dict()
        returnJson["length"] = len(imgList)
        imgPathList = [(str(ip) + "/static/" + name + "/" + i)
                       for i in imgList]
        returnJson["paths"] = imgPathList
        return returnJson



@app.route('/predict', methods=['POST'])
def upload():
    theFile = request.files.get('file')
    theName = request.data.get('fileName')
    theType = request.data.get('fileType')
    if theFile is None:
        return "Error, none has been upload"
    theFile.save(os.getcwd() + "storeImg\\file.jpg")
    return ("success")


# if __name__ == '__main__':
#     app.run(debug=True,host='1.2.3.4',port=1231)