'''
command line to to gitee clone
'''

from argparse import ArgumentParser

from git2gitee import GiteeLogin, Project, __version__


def version():
    '''return version'''
    return __version__


def cmd():
    '''
    gitee login
    if clone then clone
    '''
    ap = ArgumentParser(description='fork github repo to gitee. then clone to local.')
    ap.add_argument(dest='repo', metavar='repo')
    ap.add_argument('-u', '--username', action='store', default='mikele', help='gitee username')
    ap.add_argument('-k', '--password', action='store', help='gitee password')
    ap.add_argument('-c', '--clone', action='store_true', default=False)
    ap.add_argument('--user-agent', action='store_true', default=None)
    ap.add_argument('-v', '--version', action='version', version=__version__)
    args = ap.parse_args()

    gitee = GiteeLogin(args.username, args.password, args.user_agent)
    if gitee.login():
        project = Project(
            args.repo,
            args.username,
            gitee.sess,
            gitee.headers)
        project.check_private_duplicate()
        project.import_from_github()
        print('是否需要克隆到本地', args.clone)
        if args.clone:
            project.clone()
            project.rename_config_repo_url()


if __name__ == '__main__':
    cmd()
