import requests, json


def upload_anonfile(filename):
    url = 'https://api.anonfiles.com/upload'

    try:
        files = {'file': (open(filename, 'rb'))}
    except FileNotFoundError:
        files = ''
    except IsADirectoryError:
        files = ''
    
    if not files == '':
        r = requests.post(url, files=files)
        resp = json.loads(r.text)
        if resp['status']:
            urlshort = resp['data']['file']['url']['short']
            
            return urlshort
        
        else:
            return False

    else:
        return False


if __name__ == '__main__':
    print('Seu link de download é:', upload_anonfile('bins.db'))