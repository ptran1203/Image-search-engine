import base64
#import urllib.parse
from urllib import quote_plus
import requests


def obj_detection(path):
    # Read and encode to base64
    image = open(path, 'rb')
    image_read = image.read()
    encoded = base64.encodestring(image_read)
    dat = "data:image/jpeg;base64," + encoded.decode("utf-8")
    payload = "base64=" + quote_plus(dat)

    # Upload image
    url = "http://api.mmlab.uit.edu.vn/api/v1/file/image"
    querystring = {"method": "base64"}
    headers = {
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        'Postman-Token': "b6bd7915-3e4d-413e-892f-59917bda5a32"
    }
    req = requests.post(url, data=payload, headers=headers, params=querystring)
    file_id = str(req.json().get('fileID'))
    print file_id
    
    u = "http://api.mmlab.uit.edu.vn/api/v1/vision/object-detection?fileName=out.jpg&fileID=" + file_id + "&method=model1"
    resp = requests.get(u)
    results = resp.json().get('result')
    print results
    return results

obj_detection('./dog.jpg')