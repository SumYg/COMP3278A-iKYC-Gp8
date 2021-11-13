import logo from './logo.png';
import './App.css';
import React, {useState, useEffect} from 'react';
import {RTC2server} from "./RTCserver_connection.js"
import profilepic from './profilepic.png';
import creditcard from './creditcard.png';
import ArrayRecords from './Tables.js'
import RealTimeStockTable from './stock.js'

const pyServerAddress = 'http://localhost:8080/'

class App extends React.Component {
  constructor(props) {
    super(props)
    this.test = this.test.bind(this)
    this.change2Home = this.change2Home.bind(this)
    this.setMainState = this.setMainState.bind(this)
    this.setCurrentAccount = this.setCurrentAccount.bind(this)
    this.state = {
      pageState: 'login',
      saving: ["HKD",123],
      invest: ["12312",123,"",""],
      credit: ["123123",123],
      stock:[[]]
      // username: 'A',
      // current: 'BC',
    }
  }
  test() {
    console.log("Moved ")
  }
  setCurrentAccount(state) {
    this.setState({'currentAcc': state})
  }
  setMainState(state) {
    switch(state) {
      case 'history':
        fetch(pyServerAddress + 'allInfo').then(response => {
          if (response.status === 200) {
            response.json().then( res => {
              console.log(res)
              this.setState({'historyData': res['data'], pageState: state})
            })
          } else {
            alert("Server return status "+response.status)
          }
        })
      break
      case 'account':
        fetch(pyServerAddress + 'getSaving').then(response => {
          if (response.status === 200) {
            response.json().then( res => {
              console.log(res)
              this.setState({'saving': res['data'], pageState: state})
            })
          } else {
            alert("Server return status "+response.status)
          }
        })
        fetch(pyServerAddress + 'getCredit').then(response => {
          if (response.status === 200) {
            response.json().then( res => {
              console.log(res)
              this.setState({'credit': res['data'], pageState: state})
            })
          } else {
            alert("Server return status "+response.status)
          }
        })
        fetch(pyServerAddress + 'getInvest').then(response => {
          if (response.status === 200) {
            response.json().then( res => {
              console.log(res)
              this.setState({'invest': res['data'], pageState: state})
            })
          } else {
            alert("Server return status "+response.status)
          }
        })
      break
      case 'stock':
        fetch(pyServerAddress + 'getStock').then(response => {
          if (response.status === 200) {
            response.json().then( res => {
              console.log(res)
              this.setState({'stock': res['data'], pageState: state})
            })
          } else {
            alert("Server return status "+response.status)
          }
        })
      break
      // case 'transaction':
      //   console.log(this.state.currentAcc)
      //   fetch(pyServerAddress + 'getTransHis', {
      //     method: "POST",
      //     body: JSON.stringify([this.state.currentAcc])
      //   }).then(response => {
      //     if (response.status === 200) {
      //       response.json().then( res => {
      //         console.log(res)
      //         this.setState({'transactionHistory': res['data'], pageState: state})
      //       })
      //     } else {
      //       alert("Server return status "+response.status)
      //     }
      //   })
      //   break
      default:
      this.setState({pageState: state})
  }
  }
  change2Home() {
    fetch(pyServerAddress + 'myInfo').then(response => {
      if (response.status === 200) {
        response.json().then( res => {
          console.log(res)
          this.setState(res)
          this.setMainState('home')
        })
      } else {
        alert("Server return status "+response.status)
      }
    })
  }
  
  
  render() {
    const pageState = this.state.pageState
    let body
    switch(pageState) {
      case 'login':
        body = <LoginPage onClick={this.test} change2Home={this.change2Home}/>
        break
      case 'home':
        body = <HomePage username={this.state.username} current={this.state.current} setMainState={this.setMainState}/>
        break
      case 'account':
        body = <AccountPage setMainState={this.setMainState} saving={this.state.saving} credit={this.state.credit} invest={this.state.invest} setCurrentAccount={this.setCurrentAccount}/>
        break
      case 'history':
        body = <HistoryPage setMainState={this.setMainState} historyData={this.state.historyData}/>
        break
      case 'stock':
        body = <StockPage setMainState={this.setMainState} stock={this.state.stock}/>
        break
      case 'transaction':
        body = <TransactionPage setMainState={this.setMainState} currentAcc={this.state.currentAcc} saving={this.state.saving} credit={this.state.credit} invest={this.state.invest} setCurrentAccount={this.setCurrentAccount}/>
        break
      case 'internal':
        let currentData;
        switch(this.state.currentAcc) {
          case 'saving':
            currentData = this.state.saving
            break
          case 'credit':
            currentData = this.state.invest
            break
          default:
            currentData = this.state.credit
        }
        body = <InternalTransactionPage setMainState={this.setMainState} currentAcc={this.state.currentAcc} currentData={currentData}/>
        break
      case 'external':
        body = <ExternalTransactionPage setMainState={this.setMainState} currentAcc={this.state.currentAcc} currentData={this.state.saving}/>
        break
      
      default:
        body = null

    }
    return (
      <React.Fragment>
        {body}
      </React.Fragment>
    )
  }
}

function LogoutButton() {
  return <button id="logout-but" onClick={() => {window.location.reload()}}>Logout</button>
}

function BackToHomeButton(props) {
  return <button onClick={() => {props.setMainState('home')}}>Back To Home</button>
}
function BackToAccountButton(props) {
  return <button onClick={() => {props.setMainState('account')}}>Back To Account</button>
}
function TransactionPage(props){
  let buttons, currentNo;
  console.log("[]]")
  console.log(props.currentAcc)
  switch(props.currentAcc) {
    case 'saving':
      currentNo = props.saving[0]
      break
    case 'credit':
      currentNo = props.invest[0]
      break
    default:
      currentNo = props.credit[0]
  }
  console.log(currentNo)
  if (props.currentAcc === 'saving') {
    buttons = <React.Fragment>
    <TransButton setMainState={props.setMainState} text='External' state='external'/>
    <TransButton setMainState={props.setMainState} text='Internal' state='internal'/>
    </React.Fragment>
  } else {
    buttons = <TransButton setMainState={props.setMainState} text='Internal' state='internal'/>
  }
  function search(e) {
    let transactionid=document.getElementById("transactionid").value;
    let amountfrom=parseFloat(document.getElementById("amountfrom").value);
    let amountto=parseFloat(document.getElementById("amountto").value);
    let datefrom=document.getElementById("datefrom").value;
    let dateto=document.getElementById("dateto").value;
    let hourfrom=document.getElementById("hourfrom").value;
    let hourto=document.getElementById("hourto").value;
    let fromAccount=document.getElementById("fromAccount").value;
    let toAccount=document.getElementById("toAccount").value;
    let accountno=currentNo;
    if(amountfrom>amountto){
      [amountfrom,amountto]=[amountto,amountfrom];
      console.log("amount bigger");
    }
    if(new Date(datefrom).getTime()>new Date(dateto).getTime()){
      [datefrom,dateto]=[dateto,datefrom];
      console.log("date bigger");
    }
    fetch(pyServerAddress + 'transactionsearch', {
      method: "POST",
      body: JSON.stringify([transactionid,amountfrom,amountto,datefrom,dateto,hourfrom,hourto,
        fromAccount,toAccount,accountno])
    }).then( response => {
      if (response.status === 200) {
        response.json().then( res => {
          console.log(res)
          if (res) {
            
            // props.change2Home()
          } else {
            
          }
        })
      } else {
        alert("Server return status "+response.status)
      }
    })
    
  }
  return <div id="transaction-page">
    <h1>TransactionPage</h1>
    {props.currentAcc}
    {buttons}
    <span id="transearch">
    <table>
      <tr>
        <th>Transaction ID</th>
        <th>Amount</th>
        <th>Date:</th>
        <th>Time(h)(00-23)</th>
        <th>From Account</th>
        <th>To Account</th>
      </tr>
      <tr>
      <td><input name="transactionid" id="transactionid"></input></td>
      <td>
      <div><input name="amountfrom" id="amountfrom" placeholder="From"></input></div>
      <div><input name="amountto" id="amountto" placeholder="To"></input></div>
      </td>
      <td>
      <div><input name="datefrom" id="datefrom" placeholder="From" onFocus={(e)=>e.target.type='date'} onBlur={(e)=>e.target.type='text'}></input></div>
      <div><input name="dateto" id="dateto" placeholder="To" onFocus={(e)=>e.target.type='date'} onBlur={(e)=>e.target.type='text'}></input></div>
      </td>
      <td>
        <div><input name="hourfrom" id="hourfrom" placeholder="From"></input></div>
        <div><input name="hourto" id="hourto" placeholder="To"></input></div>
      </td>
      <td>
        <input name="fromAccount" id="fromAccount"></input>
      </td>
      <td>
        <input name="toAccount" id="toAccount"></input>
      </td>
      </tr>
     
    </table>
    </span>
    <br />
    <button onClick={search}>Search</button>
    <TransactionHistoryTable accNo={currentNo}/>
    <BackToAccountButton setMainState={props.setMainState}/>
    <LogoutButton />
  </div>
}
function TransactionHistoryTable(props) {
  const [data, setData] = useState(undefined);
  
  if (data == undefined) {
    setData([])
    fetch(pyServerAddress + 'getTransHis', {
      method: "POST",
      body: JSON.stringify([props.accNo])
    }).then(response => {
      if (response.status === 200) {
        response.json().then( res => {
          console.log(res)
          if (res.length === 0) {
            setData([['None', 'None', 'None', 'None', 'None', 'None']])
          } else {
            setData(res)
          }
        })
      } else {
        alert("Server return status "+response.status)
      }
    })
  }
  return <div id='history-div' style={{overflow: 'auto', height: '80%'}}>
  <table id='history-table' >
    <tbody>
      <tr>
        <th>Transaction ID</th>
        <th>Amount</th>
        <th>Time</th>
        <th>Date</th>
        <th>From</th>
        <th>To</th>
      </tr>
    <ArrayRecords records={data}/>
    </tbody>
  </table>
  </div>
  
}
function TransButton(props) {
  return <button onClick={() => {props.setMainState(props.state)}} id={props.state}>{props.text}</button>
}
function InternalTransactionPage(props) {
  console.log(props.currentAcc)
  console.log(props.currentData)
  let selectOptions;
  switch (props.currentAcc) {
    case 'invest':
      selectOptions = <React.Fragment>
        <option value="saving">Saving Account</option>
        <option value="credit">Credit Account</option>
      </React.Fragment>
      break
    case'saving':
      selectOptions = <React.Fragment>
        <option value="invest">Investment Account</option>
        <option value="credit">Credit Account</option>
      </React.Fragment>
      break
    default:
      selectOptions = <React.Fragment>
        <option value="saving">Saving Account</option>
        <option value="invest">Investment Account</option>
      </React.Fragment>
      break

  }
  function internaltrans(e){
    e.preventDefault();
    let amount = parseFloat(document.getElementById("amount").value);
    console.log(amount)
    let inttoAccount=document.getElementById("inttoAccount").value;
    let intfromAccount=props.currentAcc;
    let serverfunction="int"+intfromAccount+"to"+inttoAccount;
    console.log(serverfunction)
    fetch(pyServerAddress + serverfunction, {
      method: "POST",
      body: JSON.stringify([amount])
    }).then( response => {
      if (response.status === 200) {
        response.json().then( res => {
          console.log(res)
          if (res!=-1) {
            alert("Transaction Succeed")
            props.setMainState('account')
            // props.change2Home()
          } else {
            alert("Please check the amount")
          }
        })
      } else {
        alert("Server return status "+response.status)
      }
    })


  }
  return <div id='internal-page'>
    <h1>Internal</h1>
    <BackToAccountButton setMainState={props.setMainState}/>
    <LogoutButton />
    <form>
      
      <p><label htmlFor="inttoAccount">To</label>

      <select name="inttoAccount" id="inttoAccount">
        {selectOptions}
      </select></p>
      <p>
      <label htmlFor='amount'>Amount</label>
      <input name='amount' id='amount' required></input>
      </p>
      <p>
      <button onClick={internaltrans}>Submit</button>
      </p>
    </form>

  </div>
}
function ExternalTransactionPage(props) {
  console.log(props.currentAcc)
  console.log(props.currentData)
  function sendForm(e) {
    e.preventDefault()
    let amount = parseFloat(document.getElementById("amount").value)
    let exttoAccount = document.getElementById('exttoAccount').value
    fetch(pyServerAddress + 'external', {
      method: "POST",
      body: JSON.stringify([props.currentData[0], exttoAccount, amount])
    }).then( response => {
      if (response.status === 200) {
        response.json().then( res => {
          console.log(res)
          if (res) {
            alert("Transaction Succeed")
            props.setMainState('account')
            // props.change2Home()
          } else {
            alert("Please check the account number or amount")
          }
        })
      } else {
        alert("Server return status "+response.status)
      }
    })
  }
  return <div id='external-page'>
    <h1>External</h1>
    <BackToAccountButton setMainState={props.setMainState}/>
    <LogoutButton />
    <form>
      
      <p><label htmlFor="exttoAccount">Account Number:</label>
      <input name='exttoAccount' id='exttoAccount' required></input>
     
      </p>
      <p>
      <label htmlFor='amount'>Amount:</label>
      <input name='amount' id='amount'></input>
      </p>
      <p>
      <button onClick={sendForm}>Submit</button>
      </p>
    </form>
  </div>
}
function AccountPage(props) {
  return <div id='account-page'>
    <h1>Account Page</h1>
    <h2>click the accounts to see the transactions</h2>
    
    <BackToHomeButton setMainState={props.setMainState}/>
    <LogoutButton />
    <div>
      <button id="saving" onClick={()=>{props.setCurrentAccount('saving');props.setMainState('transaction')}}><div className="account-details" >Saving<span >Amount:{props.saving[1]}{props.saving[2]}</span></div></button>
      <button id="credit" onClick={()=>{props.setCurrentAccount('credit');props.setMainState('transaction')}} ><div className="account-details" >Credit <span >Balance:{props.credit[2]-props.credit[1]}</span></div></button>
      <button id="investment" onClick={()=>{props.setCurrentAccount('invest');props.setMainState('transaction')}}><div className="account-details">Investment<span >Amount: {props.invest[1]}</span></div></button>
    </div>
  </div>
}

function HistoryPage(props) {
  
  return <div id='history-page'>
    <h1>Login History</h1>
    <BackToHomeButton setMainState={props.setMainState}/>
    <LogoutButton />
    <div id='history-div' style={{overflow: 'auto', height: '80%'}}>
    <table id='history-table' >
      <tbody>
      <ArrayRecords records={props.historyData} />
      </tbody>
    </table>
    </div>
    
  </div>
}

function StockPage(props) {
  return <div id='stock-page'>
    <h1>Stock Page</h1>
    <BackToHomeButton setMainState={props.setMainState}/>
    <LogoutButton />
    <div id='stock-table-div'>
    <table id='stock-table' >
      <tbody>
        <tr>
          <th>Stock</th>
          <th>Price</th>
          <th>% Change</th>
          <th>Owned</th>
          <th>History Profit</th>
          <th>Current Value</th>
          <th>Total Spend</th>
          <th>Action</th>
        </tr>
      <RealTimeStockTable records={props.stock} />
      </tbody>
    </table>
    </div>
  </div>
}


function HomePage(props) {
  return   <div id='home-page'>
    <h1>Welcome</h1>
    <div id="outter_user_frame">
      <div id="user_frame">
        <img style={{width:'50%', maxHeight:"50%"}} src={profilepic} id="profilepic" alt='profilepic'/>
        <div id="user_frame_username">username: {props.username}</div>
        <div id="user_frame_last_login">Last login: {props.current}</div>
        
      </div>
      {/* <div>
        <img style={{width:'45%', height:"30%"}} src={creditcard} id="creditcard" alt='creditcard'/>
      </div> */}
    </div>
    <div>
    <button id="user_info" onClick={() => {props.setMainState('history')}}>User info</button>
    <button id="account_info" onClick={() => {props.setMainState('account')}}>Account info</button>
    <button id="stock_info" onClick={() => {props.setMainState('stock')}}>Stock</button>
    </div>
    <LogoutButton />
  </div>
}

function LoginPage(props) {
  function register() {
    document.getElementById("pw_login").style.display="none";
    document.getElementById("face_login").style.display="none";
    document.getElementById("register-button").style.display="none";
    document.getElementById("welcome").innerText="Please register";
    document.getElementById("record_face").style.display="block";
  }

  function record() {
    function afterTrain() {
      console.log("After Trained")
      fetch(pyServerAddress + 'insert', {
        method: "POST",
        body: JSON.stringify({username: account, password: password})
      }).then( response => {
        if (response.status === 200) {
          response.json().then( res => {
            console.log(res)
            if (res.registered) {
              props.change2Home()
            } else {
              alert('Failed to register')
            }
          })
        } else {
          alert("Server return status "+response.status)
        }
      })
    }
    var account = document.getElementById("account").value
    let password = document.getElementById('password').value
    if (account === "" || password === "") {
      alert("Please input both the account and password")
    } else {
      // assume this code cannot be changed
      fetch(pyServerAddress + 'check', {
        method: "POST",
        body: JSON.stringify({username: account})
      }).then( response => {
        if (response.status === 200) {
          response.json().then( res => {
            console.log(res)
            if (res.exist) {
              console.log('Duplicate Username')
              alert('Duplicate Username')
              document.getElementById("account").value = ''
            } else {
              console.log('Continue .')
              document.getElementById("record_face").style.display="none";
              document.getElementById("video").style.display="block";
              console.log(account)
              RTC2server(account, true, afterTrain)
              console.log('Line after RTC2server')
            }
          })
        } else {
          alert("Server return status "+response.status)
        }
      })
    }
  }
  function login() {
    // alert("loging")
    RTC2server(null, false, props.change2Home)
  }
  function passwordlogin(e) {
    e.preventDefault()
    let account = document.getElementById("account").value
    let password = document.getElementById('password').value
    fetch(pyServerAddress + 'password_login', {
      method: "POST",
      body: JSON.stringify({username: account, password: password})
    }).then( response => {
      if (response.status === 200) {
        response.json().then( res => {
          console.log(res)
          if (res.loginSucceed) {
            props.change2Home()
          } else {
            alert("Please check your account or password")
          }
        })
      } else {
        alert("Server return status "+response.status)
      }
    })
  }
  return <div id="login-page">
  <img style={{width:'300px', maxHeight:"50%"}} src={logo} id="logo" alt='logo'/>
  <h1 id="welcome">Welcome, Please Login</h1><div id="LoginANDRegister">
  <form id="loginForm"><p><label htmlFor="account">Account:</label><input type="text" id="account"></input></p><p><label htmlFor="password">Password:</label> <input type="password" id="password"></input></p>
      <button id="pw_login" onClick={passwordlogin}>Login with password</button></form>
      <button id="face_login" onClick={login}>Login with FaceID</button>
      <button id="register-button" onClick={register}>Register</button>
      <button id="record_face" style={{display: "none"}} onClick={record}>Register your face</button>
      <video width="320" height="240" id="video" autoPlay={true} playsInline={true} style={{display: "none"}}></video>
  </div>
</div>
}

export default App;