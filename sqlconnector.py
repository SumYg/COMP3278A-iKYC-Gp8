import pymysql
import datetime
from aiohttp import web


myconn = pymysql.connect(host="sophia.cs.hku.hk", user="h3566726", passwd="844328", database="h3566726")
date = datetime.datetime.utcnow()
now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()

def send_sql_to_server(query):
    print(query)
    name = cursor.execute(query)
    result = cursor.fetchall()
    myconn.commit()
    return result

# Find the customer information in the database.
def selection(request):
    select = "SELECT * FROM Customer"
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    print(current_time)
    # sql_cmd = f"INSERT INTO `Customer` (`username`, `password`) VALUES ('aaaaaa', '123')"
    sql_cmd = f"INSERT INTO `Login_History` VALUES ('{current_time}', 'edmund')"
    print(send_sql_to_server(sql_cmd))
    name = cursor.execute(select)
    result = cursor.fetchall()
    print(result)
    data = "error"
    res = dict()
    for i, r in enumerate(result):
        res[i] = r
    return web.json_response(res)
