'''
从github导入仓库到gitee
解决github下载速度慢的问题
'''

import sys
from argparse import ArgumentParser

from git2gitee.cross import Cross
from git2gitee.config import token


__author__ = 'wei40680@gmail.com'
__version__ = '0.0.4'
my_gitee = 'https://gitee.com/mikele'


def cmd():
    ap = ArgumentParser(description='fork github repo to gitee. then clone to local.')
    ap.add_argument(dest='repo', metavar='repo')
    ap.add_argument('-u', '--username', action='store', default='mikele', help='gitee username')
    ap.add_argument('-s', '--seconds', action='store', default=180)
    ap.add_argument('-t', '--token', action='store', help='gitee api token', default=token)
    ap.add_argument('-c', '--clone', action='store_true')
    args = ap.parse_args()
    gee = Cross(args.token, args.repo, args.username, timeout=args.seconds)
    gee.import_to_gitee()
    if args.clone:
        gee.clone()
        gee.rename_config_repo_url()


if __name__ == '__main__':
    cmd()
