import pymysql

#打开数据库连接
db= pymysql.connect(host="localhost",user="root",password="wpkenan",db="apple",port=3306);
# 使用cursor()方法获取操作游标
cur=db.cursor();

sql="show databass;"
try:
    cur.execute(sql);
    results=cur.fetchall();
    print(results)
except Exception as e:
    print("error->安全关闭")
    db.rollback()
    db.close();
finally:
    print("finally")