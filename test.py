import requests
import os
# import predicting_model.predict as pr
import time

url = 'http://localhost:5000/edit'

# with open('123.jpg', 'wb') as fd:
#     for chunk in r.iter_content():
#         fd.write(chunk)

files = {'file': ('222.jpg', open("test.jpg", 'rb'), 'image/jpg')}
# files = {'file': "22222111"}

# files = {'file':open('C:/Users/Owner/Desktop/Pytest/Insert-Recognition-System-Backend/testImg/1.jpg','rb')}
# data = {'fileName': "1.jpg", 'fileType': "jpg"}

# specie = pr.predict("C:/Users/WCG/Desktop/Pytest/Insert-Recognition-System-Backend/predicting_model/dataset/train/Clostera_anachoreta/1.jpg", 2, True)

# print (specie)

upJson = {
    "order": "2212312312312312322",
    "family": "22222",
    "family_code": "22222",
    "genus": "22222",
    "genus_code": "22222",
    "name": "22222",
    "pest_code": "22222",
    "latin_name": "22222",
    "plant": "22222",
    "area": "22222",
    "description": "22222"
}
timeStart = time.time()

res = requests.request("POST", url, files=files,data = upJson)

timeEnd = time.time()

timeC = timeEnd - timeStart

print(res.text)
print(timeC)

# # # print()

# print(type(Insert.query.filter_by(latin_name="micromelalopha troglodyta").all()))
# print(Insert.query.filter_by(latin_name="micromelalopha troglodyta").all().to_json())
