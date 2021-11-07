import mysql.connector
import datetime

mydb = mysql.connector.connect(
  host="sophia.cs.hku.hk",
  user="h3566726",
  password="844328",
  database="h3566726"
)

mycursor = mydb.cursor()

USER_NAME = None

def loginWithPassword(username, password):
    query = f"SELECT username FROM Customer WHERE username = '{username}' AND password= '{password}'"
    mycursor.execute(query)
    if len(mycursor.fetchall()) == 1:
        insertLoginHistory(username)
        return True
    return False

def getInfo():
    """
    Return username, First 2 latest login time
    """
    query = f"SELECT username, time FROM Login_History WHERE username = '{USER_NAME}' ORDER BY time DESC LIMIT 2"
    mycursor.execute(query)
    result = mycursor.fetchall()
    mydb.commit()
    print(result)
    return result

def checkDuplicateUser(username):
    """
    Return True when the username exist
    Else return False
    """
    query = f"SELECT username FROM Customer WHERE username = '{username}'"
    mycursor.execute(query)
    result = len(mycursor.fetchall())
    return result != 0
    
def register(username, password):
    query = f"INSERT INTO Customer (username, password) VALUES ('{username}', '{password}')"
    mycursor.execute(query)
    mydb.commit()
    createSavingAccount(username)
    createInvestAccount(username)
    createCreditAccount(username)
    print(mycursor.rowcount, "record inserted.")

def insertLoginHistory(username):
    global USER_NAME
    USER_NAME = username
    print("Set USER_NAME", USER_NAME)
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
    accNo = str(countAcount()+1).zfill(8)
    query = f"INSERT INTO Account VALUES('{accNo}', '{username}')"
    mycursor.execute(query)
    mydb.commit()
    return accNo

def createSavingAccount(username, amount=1000, current='HKD'):
    accNo = createAccount(username)
    query = f"INSERT INTO Saving VALUES('{accNo}', '{current}', {amount})"
    mycursor.execute(query)
    mydb.commit()

def createInvestAccount(username, amount=0):
    accNo = createAccount(username)
    query = f"INSERT INTO Investment VALUES('{accNo}', {amount})"
    mycursor.execute(query)
    mydb.commit()

def createCreditAccount(username, available=0, remaining=0):
    accNo = createAccount(username)
    query = f"INSERT INTO Credit VALUES('{accNo}', '{available}', '{remaining}')"
    mycursor.execute(query)
    mydb.commit()
    
#register("hhh","111")
#insertLoginHistory("John")
#changePassword("John", "abcde")
#createAccount("edmund")
#checkDuplicateUser("j")
#countAcount()
#createSavingAccount("edmund", "HKD", 0)
#createInvestAccount("edmund", 0)
#createCreditAccount("edmund", 10000, 10000)

