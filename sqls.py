import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="sophia.cs.hku.hk",
  user="h3566726",
  password="844328",
  database="h3566726"
)

def checkDuplicateUser(username):
    mycursor = mydb.cursor()
    sql = "SELECT username FROM Customer WHERE username LIKE 'edmund'"
    val = username;
    mycursor.execute(sql)
    result = mycursor.fetchall()
    print(result)
    
def register(username, password):
    sql = "INSERT INTO Customer (username, password) VALUES (%s, %s)"
    val = (username, password)
    mycursor = mydb.cursor()
    mycursor.execute(sql, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def insertLoginHistory(username):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    sql_cmd = "INSERT INTO Login_History VALUES(%s, %s)"
    val = (current_time, username)
    mycursor = mydb.cursor()
    mycursor.execute(sql_cmd, val)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def changePassword(username, newPw):
    sql_cmd = "UPDATE Customer SET password = %s WHERE username = %s"
    val = (newPw, username)
    mycursor = mydb.cursor()
    mycursor.execute(sql_cmd, val)
    mydb.commit()
    print(mycursor.rowcount, "record changed.")
    
def createAccount(username):
    sql_cmd = "INSERT INTO Account VALUES(%s, %s)"
    accNo = "00000001"
    val = (accNo, username)
    mycursor = mydb.cursor()
    mycursor.execute(sql_cmd, val)
    mydb.commit()
#register('edmund',"111")
#insertLoginHistory("John")
#changePassword("John", "abcde")
#createAccount("edmund")
checkDuplicateUser("edmund")

