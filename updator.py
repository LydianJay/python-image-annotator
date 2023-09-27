import requests



def isUpToDate():
    response = requests.get(f'https://raw.githubusercontent.com/LydianJay/python-image-annotator/main/version.txt')

    if response.status_code == 200:
        return response.text.strip()
    else:
        return "FAIL"
