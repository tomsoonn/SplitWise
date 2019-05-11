import requests
import json
import re

def send_request(content):
    URL = 'https://vision.googleapis.com/v1/images:annotate?key='

    content = {'content': content}
    features = [{'type': 'DOCUMENT_TEXT_DETECTION'}]
    img_context = {'languageHints': ['pl']}
    data = {'requests': [
        {'image': content, 'features': features, 'imageContext': img_context}]}
    req = requests.post(URL, data=json.dumps(data))
    return req.text

def find_amount(img_string):
    response_text = send_request(img_string)
    response = json.loads(response_text)["responses"][0]
    if "textAnnotations" in response:
        text = response["textAnnotations"][0]["description"]
        suma = re.search(".*SU[MHN]A PLN[ \n]([0-9]+[,.]?[0-9]*).*", text)
        if suma is not None:
            return suma.group(1)
    return 0

    