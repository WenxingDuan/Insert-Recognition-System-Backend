# import requests
# import os
# import predicting_model.predict as pr
# url = 'http://localhost:5000/predict'

# # with open('123.jpg', 'wb') as fd:
# #     for chunk in r.iter_content():
# #         fd.write(chunk)

# files = {
#     'file': ('222.jpg', open("C:\\Users\\WCG\\Desktop\\Pytest\\Insert-Recognition-System-Backend\\predicting_model\\dataset\\train\\Clostera_anachoreta\\1.jpg",
#                            'rb'), 'image/jpg')
# }
# # files = {'file': "11111111"}

# # files = {'file':open('C:/Users/Owner/Desktop/Pytest/Insert-Recognition-System-Backend/testImg/1.jpg','rb')}
# # data = {'fileName': "1.jpg", 'fileType': "jpg"}


# # specie = pr.predict("C:\\Users\\WCG\\Desktop\\Pytest\\Insert-Recognition-System-Backend\\predicting_model\\dataset\\train\\Clostera_anachoreta\\1.jpg", 2, True)

# # print (specie)

# res = requests.request("POST", url, files=files)
# print(res.text)
# # # print()

from database.database import db, Insert


a= Insert.query.all()
b=[]
for i in a:
    i = i.to_json()
    b.append(i)
print(b)
# print(type(Insert.query.filter_by(latin_name="micromelalopha troglodyta").all()))
# print(Insert.query.filter_by(latin_name="micromelalopha troglodyta").all().to_json())
