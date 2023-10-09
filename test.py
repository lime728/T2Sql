import requests
import json
import argparse


header = {
    'User-Agent':'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/116.0.0.0 Safari/537.36'
}

data = {
    "question": "今天是2023年9月11日，前两年发生在杨浦的性侵案件有多少个",
}

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', '-H', help='host to listen', default='127.0.0.1')
    parser.add_argument('--port', '-P', help='port of this service', default=6006)
    args = parser.parse_args()
    url = 'http://' + str(args.host) + ':' + str(args.port) + '/sqlcoder'
    print('输入：', data['question'])
    r = requests.post(url='http://127.0.0.1:6006/sqlcoder', headers=header, data=json.dumps(data))
    print('输出：', json.loads(r.text)["output"])
