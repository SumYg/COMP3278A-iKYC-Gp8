import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="sophia.cs.hku.hk",
  user="h3566726",
  password="844328",
  database="h3566726"
)

mycursor = mydb.cursor()

def checkDuplicateUser(username):
    sql = f'SELECT username FROM Customer WHERE username LIKE \'{username}\''
    mycursor.execute(sql)
    result = len(mycursor.fetchall())
    return result
    
def register(username, password):
    sql = "INSERT INTO Customer (username, password) VALUES (%s, %s)"
    val = (username, password)
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def insertLoginHistory(username):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql_cmd = "INSERT INTO Login_History VALUES(%s, %s)"
    val = (current_time, username)
    mycursor.execute(sql_cmd, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def changePassword(username, newPw):
    sql_cmd = "UPDATE Customer SET password = %s WHERE username = %s"
    val = (newPw, username)
    mycursor.execute(sql_cmd, val)
    mydb.commit()
    print(mycursor.rowcount, "record changed.")
    
def createAccount(username):
    sql_cmd = "INSERT INTO Account VALUES(%s, %s)"
    accNo = "00000001"
    val = (accNo, username)
    mycursor.execute(sql_cmd, val)
    mydb.commit()
#register('essdssmund',"111")
#insertLoginHistory("John")
#changePassword("John", "abcde")
#createAccount("edmund")
checkDuplicateUser("edmund")

