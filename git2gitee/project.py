'''
import to gitee, clone to local, rename config url
'''
import re
import sys
import time
import os

from git2gitee.config import params, gitee_base_url, project_url
from git2gitee.util import (
    parse_token, valib_github_repo_url, parse_repo_name, to_gitee_repo_url)


class Project:
    '''
    :params username: gitee username
    :params token: gitee csrf-token
    :params repo: github repo
    >>> from git2gitee import GiteeLogin, Project
    >>> gitee = GiteeLogin(username='mikele', password='password')
    >>> gitee.login()
    project = Project('toyourheart163/git2gitee', 'mikele', gitee.token, gitee.sess)
    project.import_from_github()
    '''
    def __init__(self, repo, username, token, sess, headers):
        self.username = username
        self.token = token
        self.headers = headers
        self.repo = repo
        self.sess = sess

    def _get_project_import_token(self):
        '''get token from project import page'''
        url_project_import = gitee_base_url + 'projects/import/url'
        resp_get_project_import = self.sess.get(url_project_import, headers=self.headers)
        self.token = parse_token(resp_get_project_import)

    def _set_new_headers(self):
        '''get project import token, set new headers'''
        self._get_project_import_token()
        new_headers = self.headers.copy()
        new_headers['X-CSRF-Token'] = self.token
        del new_headers['Upgrade-Insecure-Requests']
        del new_headers['DNT']
        self.headers = new_headers

    def check_project_duplicate(self):
        '''
        检查是否重复, 是否有人已经导入过了.
        如果有人导入过了，设置repo为另人的repo, 并退出程序
        '''
        self._set_new_headers()
        data = {'import_url': valib_github_repo_url(self.repo)}
        response = self.sess.get(project_url, params=data, headers=self.headers)
        datas = response.json()
        if datas['is_duplicate']:
            self.repo = re.search('<a.*?>(.*?)</a>', datas['message']).group(1)
            print('有人导入了: ', self.repo)
            reimport = input('是否导入到你的仓库y/n?')
            if reimport.lower() == 'n':
                os._exit(0)

    def import_from_github(self):
        '''fetch github url to gitee'''
        url = valib_github_repo_url(self.repo)
        payload = params(parse_repo_name(self.repo), self.username, self.token, url)
        print(payload)
        print('开始导入', url)
        import_url = gitee_base_url + self.username + '/projects'
        resp = self.sess.post(import_url, data=payload, headers=self.headers)
        if resp.status_code == 200:
            timeout = 180
            while not self.check_fetch():
                sys.stdout.write('\r正在导入, 请先等待>>> {}秒'.format(timeout))
                timeout -= 10
                time.sleep(10)

    def check_fetch(self):
        '''
        检查是否导入成功
        '''
        repo_name = parse_repo_name(self.repo)
        gitee_repo_url = to_gitee_repo_url(self.username, repo_name)
        gitee_url_check = gitee_repo_url + '/check_fetch'
        response = self.sess.get(gitee_url_check)
        if response['in_fetch'] == 'false':
            return False
        return True

    def clone(self):
        '''clone 到本地'''
        os.system('git clone ' + valib_github_repo_url(self.repo))

    def rename_config_repo_url(self):
        '''修改本地的git remote -v 为 import_url 的地址'''
        repo_name = parse_repo_name(self.repo)
        config = os.path.join(repo_name, '.git', 'config')
        with open(config, 'r+') as f_config:
            gitee_config = f_config.read()
            github_config = gitee_config.replace(
                to_gitee_repo_url(self.username, repo_name), valib_github_repo_url(self.repo))
            f_config.write(github_config)
            print('game over')

    def force_sync_github(self) -> int:
        '''
        force sync import url
        return:
            status -> 1
        '''
        payload = {
            "user_sync_code": '',
            "password_sync_code": '',
            "sync_wiki": "false",
            "authenticity_token": self.token
        }
        url = valib_github_repo_url(self.repo) + '/force_sync_project'
        response = self.sess.post(url, data=payload, headers=self.headers)
        return response.json()['status']
