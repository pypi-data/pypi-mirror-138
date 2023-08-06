# -*- coding: utf-8 -*-
import requests
import random
import json
from hashlib import md5
import time


class Translate:
    def __init__(self, app_id, app_key, from_lang="en", to_lang="zh"):
        self.app_id = app_id
        self.app_key = app_key
        self.from_lang = from_lang
        self.to_lang = to_lang

    def translate(self, message):
        endpoint = 'http://api.fanyi.baidu.com'
        path = '/api/trans/vip/translate'
        url = endpoint + path
        query = message
        salt = random.randint(32768, 65536)
        sign = self.make_md5(self.app_id + query + str(salt) + self.app_key)
        headers = {'Content-Type': 'application/x-www-form-urlencoded'}
        payload = {'appid': self.app_id,
                   'q': query,
                   'from': self.from_lang,
                   'to': self.to_lang,
                   'salt': salt,
                   'sign': sign}
        while True:
            try:
                resp = requests.post(url, params=payload, headers=headers)
                result = resp.text
                result = json.loads(result)
                trans_result = result.get("trans_result")
                trans_result = trans_result[0] if trans_result else {}
                trans_result = trans_result.get("dst") if trans_result else ""
                return trans_result
            except:
                time.sleep(1)

    @staticmethod
    def make_md5(s, encoding='utf-8'):
        return md5(s.encode(encoding)).hexdigest()


if __name__ == '__main__':
    pass
