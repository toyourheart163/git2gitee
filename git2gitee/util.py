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
