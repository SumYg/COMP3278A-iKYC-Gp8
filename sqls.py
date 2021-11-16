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

def createSavingAccount(username, amount=1000):
    accNo = createAccount(username)
    query = f"INSERT INTO Saving VALUES('{accNo}', {amount})"
    mycursor.execute(query)
    mydb.commit()

def createInvestAccount(username, amount=0):
    accNo = createAccount(username)
    query = f"INSERT INTO Investment VALUES('{accNo}', {amount})"
    mycursor.execute(query)
    mydb.commit()

def createCreditAccount(username, available=1000, remaining=1000):
    accNo = createAccount(username)
    query = f"INSERT INTO Credit VALUES('{accNo}', '{available}', '{remaining}')"
    mycursor.execute(query)
    mydb.commit()
    
@sendTupleAsJSON
def getSavingAccount():
    """
    Return info of user.saving account
    """
    query = f"SELECT S.account_number, S.amount FROM Account A, Saving S WHERE A.account_number = S.account_number AND A.username = '{USER_NAME}'"
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
    
def checkTransAmountFromInvest(accNo, amount):
    """
    check whether the amount in saving can complete the transaction 
    return true/false 
    """
    query = f"SELECT amount FROM Investment WHERE account_number = '{accNo}'"
    mycursor.execute(query)
    result = mycursor.fetchone()[0]
    mydb.commit()
    #print(result >= amount)
    return (result >= amount)
    
def checkTransAmountFromCredit(accNo, amount):
    """
    check whether the amount in saving can complete the transaction 
    return true/false 
    """
    query = f"SELECT remaining_credit FROM Credit WHERE account_number = '{accNo}'"
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

def updateTransHistory(amount, from_acc, to_acc):
    trans_id = str(countTrans()+1).zfill(10)
    current_date = datetime.datetime.now().strftime("%Y-%m-%d")
    current_time = datetime.datetime.now().strftime("%H:%M:%S")
    query = f"INSERT INTO Transaction VALUES('{trans_id}', '{amount}', '{current_time}', '{current_date}', '{from_acc}', '{to_acc}')"
    mycursor.execute(query)
    mydb.commit()
    print(mycursor.rowcount, "record inserted to Transaction.")
    
def updateAccount(from_acc, to_acc, trans_amount, account_type1, account_type2):
    """
    """
    #deduct money from from_account
    if (account_type1 == "Credit"):
        query1 = f"UPDATE Credit SET remaining_credit = remaining_credit-'{trans_amount}' WHERE account_number = '{from_acc}'"
    else:
        query1 = f"UPDATE {account_type1} SET amount = amount-'{trans_amount}' WHERE account_number = '{from_acc}'"
    mycursor.execute(query1)
    mydb.commit()
    print(mycursor.rowcount, "record changed.")
    
    #add money to to_account
    if (account_type2 == "Credit"):
        query2 = f"UPDATE Credit SET remaining_credit = remaining_credit+'{trans_amount}' WHERE account_number = '{to_acc}'"
    else:
        query2 = f"UPDATE {account_type2} SET amount = amount+'{trans_amount}' WHERE account_number = '{to_acc}'"
    mycursor.execute(query2)
    mydb.commit()
    print(mycursor.rowcount, "record changed.")

@getPostList
@sendDictAsJSON
def makeTransFromSaving(from_acc, to_acc, amount):
    if (amount > 0):
        if (checkTransAmountFromSaving(from_acc, amount)):
            updateTransHistory(amount, from_acc, to_acc)
            updateAccount(from_acc, to_acc, amount, "Saving", "Saving")
            return True
        else:
            print("no enough amount in your saving account")
            return False
    else:
        print("you cannot input zero or negative number")
        return False
@getPostList
@sendDictAsJSON   
def internalTransFromSavingToInvest(amount):
    from_acc=getSavingAccount()[0]
    to_acc=getInvestAccount()[0]
    if (amount > 0):
        if (checkTransAmountFromSaving(from_acc, amount)):
            updateTransHistory(amount, from_acc, to_acc)
            print(mycursor.rowcount, "record inserted to Transaction.")
            updateAccount(from_acc, to_acc, amount, "Saving", "Investment")
        else:
            print("no enough amount in your saving account")
            return -1
    else:
        print("you cannot input zero or negative number")
        return -1

@getPostList
@sendDictAsJSON        
def internalTransFromInvestToSaving(amount):
    to_acc=getSavingAccount()[0]
    from_acc=getInvestAccount()[0]
    if (amount > 0):
        if(checkTransAmountFromInvest(from_acc, amount)):
            updateTransHistory(amount, from_acc, to_acc)
            print(mycursor.rowcount, "record inserted to Transaction.")
            updateAccount(from_acc, to_acc, amount, "Investment", "Saving")
        else:
            print("no enough amount in your investment account!")
            return -1
    else:
        print("you cannot input zero or negative number")
        return -1

@getPostList
@sendDictAsJSON    
def internalTransFromSavingToCredit(amount):
    from_acc=getSavingAccount()[0]
    to_acc=getCreditAccount()[0]
    if (amount > 0):
        if (checkTransAmountFromSaving(from_acc, amount)):
            updateTransHistory(amount, from_acc, to_acc)
            print(mycursor.rowcount, "record inserted to Transaction.")
            updateAccount(from_acc, to_acc, amount, "Saving", "Credit")
        else:
            print("no enough amount in your saving account")
            return -1
    else:
        print("you cannot input zero or negative number")
        return -1

@getPostList
@sendDictAsJSON        
def internalTransFromCreditToSaving(amount):
    to_acc=getSavingAccount()[0]
    from_acc=getCreditAccount()[0]
    if (amount > 0):
        if(checkTransAmountFromCredit(from_acc, amount)):
            updateTransHistory(amount, from_acc, to_acc)
            print(mycursor.rowcount, "record inserted to Transaction.")
            updateAccount(from_acc, to_acc, amount, "Credit", "Saving")
        else:
            print("no enough credit in your credit account!")
            return -1
    else:
        print("you cannot input zero or negative number")
        return -1

@getPostList
@sendDictAsJSON    
def internalTransFromIToC(amount):
    from_acc=getInvestAccount()[0]
    to_acc=getCreditAccount()[0]
    if (amount > 0):
        if (checkTransAmountFromInvest(from_acc, amount)):
            updateTransHistory(amount, from_acc, to_acc)
            print(mycursor.rowcount, "record inserted to Transaction.")
            updateAccount(from_acc, to_acc, amount, "Investment", "Credit")
        else:
            print("no enough amount in your saving account")
            return -1
    else:
        print("you cannot input zero or negative number")
        return -1
 
@getPostList
@sendDictAsJSON 
def internalTransFromCToI(amount):
    to_acc=getInvestAccount()[0]
    from_acc=getCreditAccount()[0]
    if (amount > 0):
        if(checkTransAmountFromCredit(from_acc, amount)):
            updateTransHistory(amount, from_acc, to_acc) 
            print(mycursor.rowcount, "record inserted to Transaction.")
            updateAccount(from_acc, to_acc, amount, "Credit", "Investment")
        else:
            print("no enough credit in your credit account!")
            return -1
    else:
        print("you cannot input zero or negative number")
        return -1

@getPostList
@sendDictAsJSON
def getTransactionHistory(accNo, id, amount1, amount2, date1, date2, time1, time2, fromA, toA):
    """
    get transaction history related to the given account
    return 2d list
    """
    if (id == ''):
        idQ = ''
    else:
        idQ = f" AND transaction_id = '{id}'"
    if (date1 == ''):
        dateQ = ''
    else:
        dateQ = f" AND (date >= '{date1}' AND date <= '{date2}')"
    if (time1 == ''):
        timeQ = ''
    else:
        timeQ = f" AND (time >= '{time1}:00' AND time <= '{time2}:59')"
    if (amount1 == ''):
        amountQ = ''
    else:
        amountQ = f" AND (amount >= '{amount1}' AND amount <= '{amount2}')"

    # if (fromA == ''):
    #     fromToQ = f"(to_account = '{toA}') AND (from_account = '{accNo}' OR to_account = '{accNo}') "
    # if (toA == ''):
    #     fromToQ = f"(from_account = '{fromA}') AND (from_account = '{accNo}' OR to_account = '{accNo}')"
        
    # if (fromA == '' and toA == ''):
    #     fromToQ = f"(from_account = '{accNo}' OR to_account = '{accNo}')"
    # else:
    #     fromToQ = f"(from_account = '{accNo}' AND to_account = '{toA}') OR (from_account = '{fromA}' AND to_account = '{accNo}')"

    sqlfrom = fromA
    sqlto = toA
    logic = 'OR'
    if fromA != '' and toA != '':
        logic = 'AND'
        if fromA != accNo and toA != accNo:
            return []
    if fromA == '':
        sqlto = accNo
    
    if toA == '':
        sqlfrom = accNo
    
    

    fromToQ = f"(from_account = '{sqlfrom}' {logic} to_account = '{sqlto}')"
    print(fromToQ)

    query = f"SELECT * FROM Transaction WHERE {fromToQ}{dateQ}{timeQ}{amountQ}{idQ} ORDER BY date DESC, time DESC, amount DESC"
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
    query1 = f"SELECT I.account_number FROM Account A, Investment I WHERE A.account_number = I.account_number AND A.username = '{USER_NAME}'"
    mycursor.execute(query1)
    temp = mycursor.fetchall()
    mydb.commit()

    query = f"SELECT Stock.stock_name, Stock.live_price, Stock.percentage_change, COALESCE(Trade.no_shares, 0), COALESCE(history_profit, 0), COALESCE(Stock.live_price*Trade.no_shares, 0), COALESCE(total_spend, 0) FROM Stock LEFT outer JOIN Trade ON Trade.stock_name = Stock.stock_name and account_number = '{temp[0][0]}' ORDER BY stock_name ASC"
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
@getPostList
@sendDictAsJSON
def updatePosition(stock_name, no_shares, conditon):
    """
    condition = "Buy" or "Sell"
    return False if the users investment account dont have enough funds
    """
    query1 = f"SELECT I.account_number FROM Account A, Investment I WHERE A.account_number = I.account_number AND A.username = '{USER_NAME}'"
    mycursor.execute(query1)
    temp = mycursor.fetchall()
    mydb.commit()

    add_to_total_spend = ''
    if (int(no_shares) > 0):
        if (conditon == "Buy"):
            query2 = f"SELECT (I.amount-{no_shares}* S.live_price), {no_shares}* S.live_price from Stock S, Investment I WHERE S.stock_name = '{stock_name}' and I.account_number = '{temp[0][0]}' and I.amount >= {no_shares}* S.live_price"
            mycursor.execute(query2)
            result = mycursor.fetchall()
            mydb.commit()
            if not result:
                return False
            add_to_total_spend = f', total_spend= total_spend + {result[0][1]}'
        if (conditon == "Sell"):
            query3 = f"SELECT (I.amount + ({no_shares}* S.live_price)), {no_shares}* S.live_price FROM Investment I, Trade T, Stock S  WHERE S.stock_name = '{stock_name}' and T.stock_name = '{stock_name}' and {no_shares} <= T.no_shares and I.account_number = '{temp[0][0]}'"
            print(query3)
            mycursor.execute(query3)
            result = mycursor.fetchall()
            mydb.commit()
            print(result)
            if not result:
                print("Wt")
                return False

        symbol = '+' if conditon == "Buy" else '-'
        symbol1 = '+' if conditon == "Sell" else '-'
        query4 = f"UPDATE Investment SET amount = '{result[0][0]}' WHERE account_number = '{temp[0][0]}'"
        mycursor.execute(query4)
        mydb.commit()
        stock_name, temp[0][0]
        # (stock_name, account_number, no_shares, history_profit) 
        query5 = f"INSERT INTO Trade VALUES('{stock_name}', '{temp[0][0]}', {no_shares}, -{result[0][1]}, {result[0][1]}) ON DUPLICATE KEY UPDATE no_shares= no_shares {symbol} {no_shares}, history_profit= history_profit {symbol1} {result[0][1]}{add_to_total_spend}"
        print(query5)
        # query5 = f"UPDATE Trade SET no_shares = no_shares {symbol} '{no_shares}' WHERE account_number = '{temp[0][0]}' AND stock_name = '{stock_name}'"
        mycursor.execute(query5)
        mydb.commit()
        print(temp[0][0],"Investment account updated")
        return True
    else:
        return False
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
#getTransactionHistoryYMD("00000001", "2021", "11", '08')

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
#buyStock("AAPL", 2)
#internalTransFromSavingToCredit(10000)
#internalTransFromCreditToSaving(10000)
#internalTransFromSavingToInvest(5000)
# internalTransFromInvestToSaving(5000)
#getTransactionHistory("00000001", "", "", "", "", 1, 10, "00000004", "00000005")
