import mysql.connector
import datetime


myconn = mysql.connector.connect(host="sophia.cs.hku.hk", user="h3566726", passwd="844328", database="h3566726")
date = datetime.datetime.utcnow()
now = datetime.datetime.now()
current_time = now.strftime("%H:%M:%S")
cursor = myconn.cursor()

# Find the customer information in the database.
def selection(request):
    select = "SELECT username FROM Customer WHERE username='edmund'"
    name = cursor.execute(select)
    result = cursor.fetchall()
    print(result)
    data = "error"