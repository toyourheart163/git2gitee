# git2gitee

从github导入仓库到gitee
解决github下载速度慢的问题
由于码云不提供导入的api，只能JS逆向码云登陆，导入仓库


### 安装

```bash
pip install git2gitee
```

### 使用

```bash
# git2gitee -u {gitee_username} -k {gitee_password} github_repo_url
git2gitee -u mikele -k password https://github.com/toyourheart163/git2gitee
```


### 加密方法

>进入登陆页面时会加载一个encrypt开头的js文件

#### python 使用公钥加密的方法, 使用`pycryptodome`

```python
# git2gitee/util.py
from base64 import b64encode

from Crypto.PublicKey import RSA
from Crypto.Cipher import PKCS1_v1_5

def encrypt_pwd(password, public_key):
    rsa_key = RSA.import_key(public_key)
    encryptor = PKCS1_v1_5.new(rsa_key)
    cipher = b64encode(encryptor.encrypt(password.encode('utf-8')))
    return cipher.decode('utf-8')
```

### 解决csrf-token 的问题

```python
import re

result = re.search('<meta content="(.*?)" name="csrf-token"', response.text)
token = result.group(1)
```
