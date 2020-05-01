'''
example
'''

from git2gitee.cross import Cross


if __name__ == '__main__':
    gee = Cross(args.token, args.repo, args.username, timeout=args.seconds)
    gee.import_to_gitee()
    gee.clone()
    gee.rename_config_repo_url()
