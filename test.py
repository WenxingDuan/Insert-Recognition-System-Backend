import requests
import os
url = 'http://localhost:5000/predict'
r = requests.get(url, stream=True)
# with open('123.jpg', 'wb') as fd:
#     for chunk in r.iter_content():
#         fd.write(chunk)

files = {
    'file': ('222.jpg', open('C:\\Users\\Owner\\Pictures\\222.jpg',
                           'rb'), 'image/jpg')
}
# files = {'file': "11111111"}

# files = {'file':open('C:/Users/Owner/Desktop/Pytest/Insert-Recognition-System-Backend/testImg/1.jpg','rb')}
# data = {'fileName': "1.jpg", 'fileType': "jpg"}

res = requests.request("POST", url, files=files)

# print()