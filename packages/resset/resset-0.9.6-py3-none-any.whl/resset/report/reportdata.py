import requests
import json
from resset.__config import *

def ressetLogin(loginname,loginpwd):
    login_url=decrypt(loginurl)
    url=login_url%(loginname,loginpwd)
    # print(url)
    s=requests.get(url).json()
    state=str(s['State'])
    if state=='1':
        print(s['Msg'])
    else:
        print(s['Msg'])
def get_Content_data(code,content_type, type, year):
    content_url=decrypt(contenturl)
    url=content_url%(code, content_type,type, year)
    # print(url)
    s=requests.get(url).json()
    state=str(s['State'])
    if state=='1':
        return json.loads(s['Data']) ['response']['docs']
    else:
        print(s['Msg'])
if __name__ == '__main__':
    thsLogin = ressetLogin("zhangq", "123")
    s=get_Content_data('000002','part',  '年度报告', '2011')
    print(s)