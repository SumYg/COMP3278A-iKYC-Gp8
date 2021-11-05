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
    query = f"SELECT username FROM Customer WHERE username = '{username}'"
    mycursor.execute(query)
    result = len(mycursor.fetchall())
    return result
    
def register(username, password):
    query = f"INSERT INTO Customer (username, password) VALUES ('{username}', '{password}')"
    mycursor.execute(query)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def insertLoginHistory(username):
    current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    query = f"INSERT INTO Login_History VALUES('{current_time}', '{username}')"
    mycursor.execute(query)
    mydb.commit()
    print(mycursor.rowcount, "record inserted.")

def changePassword(username, newPw):
    query = "UPDATE Customer SET password = %s WHERE username = %s"
    val = (newPw, username)
    mycursor.execute(query, val)
    mydb.commit()
    print(mycursor.rowcount, "record changed.")

def countAcount():
    query = f"SELECT COUNT(*) FROM Account"
    mycursor.execute(query)
    result = mycursor.fetchone()[0]
    #print(result)
    return result
    
def createAccount(username):
    query = "INSERT INTO Account VALUES(%s, %s)"
    accNo = str(countAcount()+1).zfill(8)
    val = (accNo, username)
    mycursor.execute(query, val)
    mydb.commit()
    
#register("hhh","111")
#insertLoginHistory("John")
#changePassword("John", "abcde")
createAccount("edmund")
#checkDuplicateUser("j")
#countAcount()

