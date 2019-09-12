import requests

'''
这是一个自动执行脚本
用来解锁被封的IP
每天0点执行
通过对接口进行访问的方式
'''

def unlockIP():
    requests.delete('https://algyun.cn:81/autoAPI/IP/')

if __name__ == '__main__':
    unlockIP()