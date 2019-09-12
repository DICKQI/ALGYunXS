# import pymysql
import requests

# Create your views here.
'''
    这个脚本用来重置所有ip的单位时间内访问次数
    直接操作数据库
    每5分钟重置一次
'''
def resetIP():
    requests.get('https://algyun.cn:81/autoAPI/IP/')

if __name__ == '__main__':
    resetIP()
