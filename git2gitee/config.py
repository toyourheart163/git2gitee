
token = '16604e967d52281868a18b0300670a43'

def params(repo, username, token, import_url):
    return {
        'utf8': '✓',
        'authenticity_token': token,
        'project[name]': repo,
        'project[namespace_path]': username,
        'project[path]': repo,
        'project[public]': '1',
        'language': '0',
        'ignore': 'no',
        'license': 'no',
        'model': '1',
        'prod': 'master',
        'dev': 'develop',
        'feat': 'feature',
        'rel': 'release',
        'bugfix': 'hotfix',
        'project[import_url]': import_url
    }
