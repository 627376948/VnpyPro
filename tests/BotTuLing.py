#author: hanshiqiang365

import json
import urllib.request


def getHtml(url):
    page = urllib.request.urlopen(url)
    html = page.read()
    return html


if __name__ == '__main__':
    key = 'ac8d3447bfca4b328d5a9170af59474d'
    api = 'http://www.tuling123.com/openapi/api?key=' + key + '&info='

    while True:
        info = input('我: ')
        request = api + str(info.encode('utf-8'))
        response = getHtml(request)
        dic_json = json.loads(response)
        print('机器人: ' + dic_json['text'])
