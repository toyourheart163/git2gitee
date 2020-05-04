'''
encrypt by public key
'''

import re
from base64 import b64encode

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5


def encrypt_pwd(password, public_key):
    '''
    :params public_key:
        -----BEGIN PUBLIC KEY----\nkeys\n-----END ...-----
    :params password: csrf-token + '$gitee$' + password
    '''
    rsa_key = RSA.import_key(public_key)
    encryptor = PKCS1_v1_5.new(rsa_key)
    cipher = b64encode(encryptor.encrypt(password.encode('utf-8')))
    return cipher.decode('utf-8')


def parse_token(response):
    '''parse csrf token form gitee'''
    result = re.search('<meta content="(.*?)" name="csrf-token"', response.text)
    return result.group(1)


def valib_github_repo_url(repo):
    '''return repo url'''
    # protocols = ('git', 'https')
    github_base_url = 'https://github.com/'
    if repo.startswith(github_base_url):
        return repo
    return github_base_url + repo


def parse_repo_name(repo):
    '''parse repo name'''
    return repo.split('/')[-1:][0]


def to_gitee_repo_url(username, repo_name):
    '''
    :params username: gitee username
    :params repo_name:  import repo name
    return gitee repo url
    '''
    return 'https://gitee.com/{}/{}'.format(username, repo_name)
