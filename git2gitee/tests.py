'''
test
'''

import os

from git2gitee.login import GiteeLogin


def test_login():
    '''test login to gitee'''
    username = 'mikele'
    password = os.getenv('GITEE_PWD')
    gitee = GiteeLogin(username, password)
    if gitee.login():
        print('登陆成功')


if __name__ == '__main__':
    test_login()
