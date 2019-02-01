import pymysql

# Create your views here.
'''
    这个脚本用来重置所有ip的单位时间内访问次数
    直接操作数据库
    每5分钟重置一次
'''
def resetIP():
    db = pymysql.connect('localhost', 'root', 'macbook123456', 'ALGYunXS')

    cursor = db.cursor()

    sql = "select * from log_visitlog"

    try:
        cursor.execute(sql)
        result = cursor.fetchall()
        for row in result:
            if row[4] == 0:
                try:
                    sql = "update log_visitlog set five_min_visit = 0 where ip='%s'" % row[1]
                    cursor.execute(sql)
                    db.commit()
                except:
                    raise Exception
    except:
        raise Exception
    db.close()

if __name__ == '__main__':
    resetIP()