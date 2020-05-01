'''
example
'''

from git2gitee.cross import Cross
from git2gitee.config import token


if __name__ == '__main__':
    gee = Cross(token, 'toyourheart163/seeing')
    gee.import_to_gitee()
    gee.clone()
    gee.rename_config_repo_url()
