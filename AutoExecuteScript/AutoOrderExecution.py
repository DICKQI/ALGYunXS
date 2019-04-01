import requests


# def deleteUnPayOrder():
#     requests.delete('https://algyun.cn:81/autoAPI/commodity/order/')


def ConfirmOvertimeOrder():
    requests.get('https://algyun.cn/autoAPI/commodity/order/')


if __name__ == '__main__':
    # deleteUnPayOrder()
    ConfirmOvertimeOrder()
