'''
import to gitee, clone to local, rename config url
'''
import os
import re
import requests
import sys
import time

from git2gitee.config import params, token


class Cross:
    '''
    :params username: gitee username
    :params repo: github repo
    :params token: gitee api token
    '''
    def __init__(self, token, repo, username='mikele', timeout=180):
        self.username = username
        self.token = token
        self.repo = repo
        self.repo_name = self.repo.split('/')[-1:][0]
        self.timeout = timeout
        self.sess = requests.Session()
        self.headers={'Authorization': 'Token ' + token}

    def valib_repo_url(self) -> str:
        '''return repo url'''
        protocols = ('git', 'https')
        github_base_url = 'https://github.com/'
        if self.repo.startswith(github_base_url):
            return self.repo
        else:
            return github_base_url + self.repo

    def import_to_gitee(self):
        '''fetch github url to gitee'''
        url = self.import_url = self.valib_repo_url()
        form = params(self.repo_name, self.username, self.token, url)
        print('开始导入')
        r = self.sess.post(url, data=form, headers=self.headers, timeout=2)
        if r.status_code == 200:
            timeout = int(self.timeout)
            while not self.check_fetch():
                sys.stdout.write('\r正在导入, 请先等待>>> {}秒'.format(timeout))
                timeout -= 10
                time.sleep(10)

    def check_fetch(self):
        # 检查是否导入成功
        self.gitee_url = 'https://gitee.com/{}/{}'.format(self.username, self.repo_name)
        gitee_url_check = self.gitee_url + '/{name}/check_fetch'.format(name=self.repo_name)
        r = self.sess.get(gitee_url_check)
        return False if r['in_fetch'] == 'false' else True

    def clone(self):
        # clone 到本地
        os.system('git clone ' + self.valib_repo_url())

    def rename_config_repo_url(self):
        # 修改本地的git remote -v 为 import_url 的地址
        config = os.path.join(self.repo_name, '.git', 'config')
        with open(config, 'r+') as f:
            gitee_config = f.read()
            github_config = gitee_config.replace(self.gitee_url, self.import_url)
            f.write(github_config)
            print('game over')

    def force_sync_github(self) -> int:
        '''
        force sync import url
        return:
            status -> 1
        '''
        params = {
            "user_sync_code": '',
            "password_sync_code": '',
            "sync_wiki": "false",
            "authenticity_token": self.token
        }
        url = self.valib_repo_url() + '/force_sync_project'
        r = self.sess.post(url, data=params, headers=self.headers)
        return r.json()['status']
