import mysql.connector
import datetime
from server import sendTupleAsJSON, getPostList, sendDictAsJSON

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
    
@sendTupleAsJSON
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

@sendTupleAsJSON
def getCreditAccount():
    """
    Return info of user.credit account
    """
    query = f"SELECT C.account_number, C.available_credit, C.remaining_credit, (C.available_credit - C.remaining_credit) as Debt FROM Account A, Credit C WHERE A.account_number = C.account_number AND A.username = '{USER_NAME}'"
    mycursor.execute(query)
    result = mycursor.fetchone()
    mydb.commit()
    print(result)
    return result

@sendTupleAsJSON
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

@getPostList
@sendDictAsJSON
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
        return True
    return False

  def updateInternalAccountFromS(accNo, trans_amount, fromOrTo):
    """
    fromOrTo == 0 -> update from_account
    fromOrTo == 1 -> update to_account
    """
    if fromOrTo == 0:
        query = f"UPDATE Saving SET amount = amount-'{trans_amount}' WHERE account_number = '{accNo}'"
    elif fromOrTo == 1:
        query = f"UPDATE Investment SET amount = amount+'{trans_amount}' WHERE account_number = '{accNo}'"
    mycursor.execute(query)
    mydb.commit()
    print(mycursor.rowcount, "record changed.")
    
def updateInternalAccountFromI(accNo, trans_amount, fromOrTo):
    """
    fromOrTo == 0 -> update from_account
    fromOrTo == 1 -> update to_account
    """
    if fromOrTo == 0:
        query = f"UPDATE Investment SET amount = amount-'{trans_amount}' WHERE account_number = '{accNo}'"
    elif fromOrTo == 1:
        query = f"UPDATE Saving SET amount = amount+'{trans_amount}' WHERE account_number = '{accNo}'"
    mycursor.execute(query)
    mydb.commit()
    print(mycursor.rowcount, "record changed.")    
    
def internalTransFromSavingToInvest(amount):
    from_acc=getSavingAccount()[0]
    to_acc=getInvestAccount()[0]
    if (checkTransAmountFromSaving(from_acc, amount)):
        trans_id = str(countTrans()+1).zfill(10)
        current_date = datetime.datetime.now().strftime("%Y-%m-%d")
        current_time = datetime.datetime.now().strftime("%H:%M:%S")
        query = f"INSERT INTO Transaction VALUES('{trans_id}', '{amount}', '{current_time}', '{current_date}', '{from_acc}', '{to_acc}')"
        mycursor.execute(query)
        mydb.commit()
        print(mycursor.rowcount, "record inserted to Transaction.")
        updateInternalAccountFromS(from_acc, amount, 0)
        updateInternalAccountFromS(to_acc, amount, 1)
    else:
        return -1
        
def internalTransFromInvestToSaving(amount):
    to_acc=getSavingAccount()[0]
    from_acc=getInvestAccount()[0]
    
    trans_id = str(countTrans()+1).zfill(10)
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    query = f"INSERT INTO Transaction VALUES('{trans_id}', '{amount}', '{current_time}', '{current_date}', '{from_acc}', '{to_acc}')"
    mycursor.execute(query)
    mydb.commit()
    print(mycursor.rowcount, "record inserted to Transaction.")
    updateInternalAccountFromI(from_acc, amount, 0)
    updateInternalAccountFromI(to_acc, amount, 1)

@getPostList
@sendDictAsJSON
def getTransactionHistory(accNo):
    """
    get transaction history related to the given account
    return 2d list
    """
    print(accNo)
    query = f"SELECT * FROM Transaction WHERE from_account = '{accNo}' OR to_account = '{accNo}' ORDER BY date DESC, time DESC, amount DESC"
    mycursor.execute(query)
    result = [[i[0], i[1], str(i[2]), str(i[3]), i[4], i[5]] for i in mycursor.fetchall()]
    mydb.commit()
    print(result)
    return result
def getTransactionHistoryYMD(accNo, year, month, day):
    """
    get transaction history related to the given account
    in a given year, month and date e.g. 20211107
    return 2d list
    """
    date = f"{year}{month}{day}"
    query = f"SELECT * FROM Transaction WHERE (from_account = '{accNo}' OR to_account = '{accNo}') AND date = '{date}'"
    mycursor.execute(query)
    result = [[i[0], i[1], str(i[2]), str(i[3]), i[4], i[5]] for i in mycursor.fetchall()]
    mydb.commit()
    print(result)
    return result
    
def getTransactionHistoryYM(accNo, year, month):
    """
    get transaction history related to the given account
    in a given year and month e.g. from 20211101 to 20211131
    return 2d list
    """
    from_date = f"{year}{month}01"
    to_date = f"{year}{month}31"
    query = f"SELECT * FROM Transaction WHERE (from_account = '{accNo}' OR to_account = '{accNo}') AND (date >= '{from_date}' AND date <= '{to_date}')"
    mycursor.execute(query)
    result = [[i[0], i[1], str(i[2]), str(i[3]), i[4], i[5]] for i in mycursor.fetchall()]
    mydb.commit()
    print(result)
    return result
 
def createStock(stock_name, live_price, percentage_change):
    query = f"INSERT INTO Stock VALUES('{stock_name}','{live_price}','{percentage_change}')"
    mycursor.execute(query)
    mydb.commit()
    print("stock ", stock_name, " created" )
    

def updateStock(stock_name, live_price, percentage_change):
    query = f"UPDATE Stock SET live_price = '{live_price}', percentage_change = '{percentage_change}' WHERE stock_name = '{stock_name}'"
    mycursor.execute(query)
    mydb.commit()
    print(mycursor.rowcount, "stock record changed.")
@sendTupleAsJSON
def getStock():
    """
    Return a json file of stock_name, live_price and precentage_change
    """
    query = f"SELECT * FROM Stock"
    mycursor.execute(query)
    result = mycursor.fetchall()
    mydb.commit()
    #print(result)
    return result

def getRealTimeStock():
    """
    Return a json file of stock_name, live_price and precentage_change
    """
    query = f"SELECT * FROM Stock"
    mycursor.execute(query)
    result = mycursor.fetchall()
    mydb.commit()
    #print(result)
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
#makeTransFromSaving("getSavingAccount()", "00000007", 100)
#getAccountType("00000001")
#getTransactionHistory("00000001")
#getAllInfo()()
#getTransactionHistoryYMD("00000001", "2021", "11", "08")
getTransactionHistoryYMD("00000001", "2021", "11", '08')

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
# makeTransFromSaving("00000001", "00000007", 100)

# getStock(0)
