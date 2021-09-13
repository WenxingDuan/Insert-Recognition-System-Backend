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

baseDir = "database"

app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    baseDir, 'inserts.sqlite')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

insertList = os.listdir("static")


@app.route('/imageList/<name>', methods=['GET'])
def imageList(name):
    if name not in insertList:
        return None
    else:
        path = "static/" + name
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
    imgPath = "storeImg/" + theName
    theFile.save(imgPath)
    specie = pr.predict(imgPath, 2)
    print('6', file=sys.stderr)
    specieJson = Insert.query.filter_by(latin_name=specie).first().to_json()
    print('7', file=sys.stderr)
    return str(specieJson).replace("\'", "\"")


@app.route('/all', methods=['GET'])
def all():
    inserts = Insert.query.all()
    insertJsonList = []
    for i in inserts:
        i = i.to_json()
        insertJsonList.append(i)
    return str(insertJsonList).replace("\'", "\"")


@app.route('/edit', methods=['POST'])
def edit():

    theFile = request.files.get('file')
    theName = theFile.filename
    imgPath = os.path.dirname(
        __file__) + "/static/" + request.form["latin_name"] + "/" + theName

    if os.path.exists("static/" + request.form["latin_name"]) == False:
        os.makedirs("static/" + request.form["latin_name"])
        theFile.save(imgPath)
        currInsert = Insert(order=request.form["order"],
                            family=request.form["family"],
                            family_code=request.form["family_code"],
                            genus=request.form["genus"],
                            genus_code=request.form["genus_code"],
                            name=request.form["name"],
                            pest_code=request.form["pest_code"],
                            latin_name=request.form["latin_name"],
                            plant=request.form["plant"],
                            area=request.form["area"],
                            description=request.form["description"],
                            link="static/" + request.form["latin_name"] + "/" +
                            theName)
        db.session.add(currInsert)
        db.session.commit()
        return ("Create Success")

    else:
        currInsert = Insert.query.filter_by(
            latin_name=request.form["latin_name"]).first()
        currInsert.order = request.form["order"]
        currInsert.family = request.form["family"]
        currInsert.family_code = request.form["family_code"]
        currInsert.genus_code = request.form["genus_code"]
        currInsert.name = request.form["name"]
        currInsert.pest_code = request.form["pest_code"]
        currInsert.latin_name = request.form["latin_name"]
        currInsert.plant = request.form["plant"]
        currInsert.area = request.form["area"]
        currInsert.description = request.form["description"]
        db.session.commit()
        return ("Edit Success")


@app.route('/delete/<latin_name>', methods=['GET'])
def delete(latin_name):
    try:
        currInsert = Insert.query.filter_by(latin_name=latin_name).first()
        db.session.delete(currInsert)
        db.session.commit()
        return ("success")
    except:
        return ("fail")


@app.route('/predictPercentage', methods=['POST'])
def predictPercentage():
    theFile = request.files.get('file')
    theName = theFile.filename
    imgPath = "storeImg/" + theName
    theFile.save(imgPath)
    #TODO: finish predictPercentage method
    specieDict = pr.predictPercentage(imgPath, 2)
    return str(specieDict).replace("\'", "\"")


@app.route('/info/<latin_name>', methods=['GET'])
def info(latin_name):
    specieJson = Insert.query.filter_by(
        latin_name=latin_name).first().to_json()
    return str(specieJson).replace("\'", "\"")


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80)
