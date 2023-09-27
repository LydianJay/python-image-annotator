import requests



def isUpToDate():
    response = requests.get(f'https://raw.githubusercontent.com/LydianJay/python-image-annotator/main/version.txt')

    if response.status_code == 200:
        print(response.text.strip())
        return response.text.strip()
    
    else:
        print("Fail")
        return "FAIL"
