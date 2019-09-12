import requests

'''
这是一个自动执行脚本
用来自动确认收货
每1分钟执行一次
通过对接口进行访问的方式
'''

def ConfirmOvertimeOrder():
    requests.get('https://algyun.cn:81/autoAPI/commodity/order/')

def CompleteTimeOrder():
    requests.delete('https://algyun.cn:81/autoAPI/commodity/order/')

if __name__ == '__main__':
    CompleteTimeOrder()
    ConfirmOvertimeOrder()
