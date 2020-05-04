'''
command line to to gitee clone
'''

from argparse import ArgumentParser

from git2gitee import GiteeLogin, Project


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
    args = ap.parse_args()

    gitee = GiteeLogin(args.username, args.password, args.user_agent)
    if gitee.login():
        print('登陆成功')
        project = Project(
            args.repo,
            args.username,
            gitee.token,
            gitee.sess,
            gitee.headers)
        project.check_project_duplicate()
        project.import_from_github()
        print(args.clone)
        if args.clone:
            project.clone()
            project.rename_config_repo_url()


if __name__ == '__main__':
    cmd()
