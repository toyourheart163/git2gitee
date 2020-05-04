'''
设置好headers
JS逆向码云
1. 获取csrf-token
2. 加密密码 token + '$gitee$' + password
'''

import json
import re

from requests import Session
from git2gitee.util import encrypt_pwd
from git2gitee.config import headers, gitee_base_url


class GiteeLogin:
    '''login to gitee'''
    def __init__(self, username='mikele', password=None, user_agent=None):
        self.username = username
        self.password = password
        self.headers = headers
        self.sess = Session()
        if user_agent:
            self.headers.update({'User-Agent': user_agent})
        self.token = None
        self.public_key = None

    def get_crsf_token(self):
        '''
        set crsf_token
        '''
        url = gitee_base_url + 'login'
        print(url, headers)
        response = self.sess.get(url, headers=self.headers)
        print(response.status_code)
        self.token = re.search('<meta content="(.*?)" name="csrf-token"', response.text).group(1)
        self.public_key = json.loads(
            re.search('gon.encrypt=(.*?);', response.text).group(1))['password_key']

    def login(self):
        '''
        Post login page to use login Session
        '''
        self.get_crsf_token()
        password = encrypt_pwd(self.token + '$gitee$' + self.password, self.public_key)
        payload = {
            'encrypt_key': 'password',
            'utf-8': '✓',
            'authenticity_token': self.token,
            'redirect_to_url': '',
            'user[login]': self.username,
            'user[remember_me]': '0',
            'encrypt_data[user[password]]': password
        }
        response = self.sess.post(gitee_base_url + 'login', data=payload, headers=self.headers)
        if self.username in response.text:
            # login success
            return True
        return None
