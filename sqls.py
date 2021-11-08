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
    Return username, latest login time
    """
    query = f"SELECT username, time FROM Login_History WHERE username = '{USER_NAME}' ORDER BY time DESC LIMIT 1 OFFSET 1"
    mycursor.execute(query)
    result = mycursor.fetchall()
    mydb.commit()
    print('Result: ',result)
    return result

def getAllInfo():
    """
    Return username, all login time
    """
    query = f"SELECT time FROM Login_History WHERE username = '{USER_NAME}' ORDER BY time DESC"
    mycursor.execute(query)
    result = mycursor.fetchall()
    mydb.commit()
    result = [time[0].strftime("%Y-%m-%d %H:%M:%S") for time in result]
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

def createSavingAccount(username, current='HKD', amount=1000):
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
    
def getSavingAccount():
    """
    Return info of user.saving account
    """
    query = f"SELECT S.account_number, S.currency, S.amount FROM Account A, Saving S WHERE A.account_number = S.account_number AND A.username = '{USER_NAME}'"
    mycursor.execute(query)
    result = mycursor.fetchone()
    mydb.commit()
    print(result)
    return result
    
def getCreditAccount():
    """
    Return info of user.credit account
    """
    query = f"SELECT C.account_number, C.available_credit, C.remaining_credit FROM Account A, Credit C WHERE A.account_number = C.account_number AND A.username = '{USER_NAME}'"
    mycursor.execute(query)
    result = mycursor.fetchone()
    mydb.commit()
    print(result)
    return result
    
def getInvestAccount():
    """
    Return account number, amount in table Investment 
    """
    query = f"SELECT I.account_number, I.amount FROM Account A, Investment I WHERE A.account_number = I.account_number AND A.username = '{USER_NAME}'"
    mycursor.execute(query)
    result = mycursor.fetchone()
    mydb.commit()
    print(result)
    return result
    
def getOwnerOfAccount(accNo):
    """
    Return username
    """
    query = f"SELECT username FROM Account WHERE account_number = '{accNo}'"
    mycursor.execute(query)
    result = mycursor.fetchone()[0]
    mydb.commit()
    #print(result)
    return result

def checkTransAmountFromSaving(accNo, amount):
    """
    check whether the amount in saving can complete the transaction 
    return true/false 
    """
    query = f"SELECT amount FROM Saving WHERE account_number = '{accNo}'"
    mycursor.execute(query)
    result = mycursor.fetchone()[0]
    mydb.commit()
    #print(result >= amount)
    return (result >= amount)

def countTrans():
    query = f"SELECT COUNT(*) FROM Transaction"
    mycursor.execute(query)
    result = mycursor.fetchone()[0]
    #print(result)
    return result

def updateAccount(accNo, trans_amount, fromOrTo):
    """
    fromOrTo == 0 -> update from_account
    fromOrTo == 1 -> update to_account
    """
    if fromOrTo == 0:
        query = f"UPDATE Saving SET amount = amount-'{trans_amount}' WHERE account_number = '{accNo}'"
    elif fromOrTo == 1:
        query = f"UPDATE Saving SET amount = amount+'{trans_amount}' WHERE account_number = '{accNo}'"
    mycursor.execute(query)
    mydb.commit()
    print(mycursor.rowcount, "record changed.")

def makeTransFromSaving(from_acc, to_acc, amount):
    if (checkTransAmountFromSaving(from_acc, amount)):
        trans_id = str(countTrans()+1).zfill(10)
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        query = f"INSERT INTO Transaction VALUES('{trans_id}', '{amount}', '{current_time}', '{current_date}', '{from_acc}', '{to_acc}')"
        mycursor.execute(query)
        mydb.commit()
        print(mycursor.rowcount, "record inserted to Transaction.")
        updateAccount(from_acc, amount, 0)
        updateAccount(to_acc, amount, 1)
    else:
        return -1
      
def getTransactionHistory(accNo):
    """
    get transaction history related to the given account 
    """
    query = f"SELECT * FROM Transaction WHERE from_account = '{accNo}' OR to_account = '{accNo}'"
    mycursor.execute(query)
    result = [[i[0], i[1], str(i[2]), str(i[3]), i[4], i[5]] for i in mycursor.fetchall()]
    mydb.commit()
    print(result)
    return result
  
#register("hhh","111")
#insertLoginHistory("John")
#changePassword("John", "abcde")
#createAccount("edmund")
#checkDuplicateUser("j")
#countAcount()
#createSavingAccount("edmund", "HKD", 0)
#createInvestAccount("edmund", 0)
#createCreditAccount("edmund", 10000, 10000)
USER_NAME = "edmund"
#getAllInfo()
#getSavingAccount()
#getCreditAccount()
#getInvestAccount()
#getOwnerOfAccount("00000001")
#checkTransAmountFromSaving(getSavingAccount()[0], 1000)
makeTransFromSaving("00000001", "00000007", 100)
