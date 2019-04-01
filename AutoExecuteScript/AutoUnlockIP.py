import requests

def unlockIP():
    requests.delete('https://algyun.cn:81/autoAPI/IP/')

if __name__ == '__main__':
    unlockIP()