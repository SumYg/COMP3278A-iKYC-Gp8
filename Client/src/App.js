import logo from './logo.png';
import './App.css';
import React from 'react';
import {RTC2server} from "./RTCserver_connection.js"
import profilepic from './profilepic.png';
import creditcard from './creditcard.png';
import ArrayRecords from './Tables.js'
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
      credit: ["123123",123]
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
              this.setState({'historyData': res['data']})
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
              this.setState({'saving': res['data']})
            })
          } else {
            alert("Server return status "+response.status)
          }
        })
        fetch(pyServerAddress + 'getCredit').then(response => {
          if (response.status === 200) {
            response.json().then( res => {
              console.log(res)
              this.setState({'credit': res['data']})
            })
          } else {
            alert("Server return status "+response.status)
          }
        })
        fetch(pyServerAddress + 'getInvest').then(response => {
          if (response.status === 200) {
            response.json().then( res => {
              console.log(res)
              this.setState({'invest': res['data']})
            })
          } else {
            alert("Server return status "+response.status)
          }
        })
      break
      default:  // do nothing
    }
    this.setState({pageState: state})
  }
  change2Home() {
    fetch(pyServerAddress + 'myInfo').then(response => {
      if (response.status === 200) {
        response.json().then( res => {
          console.log(res)
          this.setState(res)
        })
      } else {
        alert("Server return status "+response.status)
      }
    })
    this.setMainState('home')
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
        body = <StockPage setMainState={this.setMainState}/>
        break
      case 'transaction':
        body = <TransactionPage setMainState={this.setMainState} currentAcc={this.state.currentAcc}/>
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
function TransactionPage(props){
  let buttons;
  if (props.currentAcc == 'saving') {
    buttons = [<TransButton setMainState={props.setMainState} text='External' state='external'/>, <TransButton setMainState={props.setMainState} text='Internal' state='internal'/>]
  } else {
    buttons = <TransButton setMainState={props.setMainState} text='Internal' state='internal'/>
  }
  return <div id="transaction-page">
    <h1>TransactionPage</h1>
    {props.currentAcc}
    {buttons}
    <BackToHomeButton setMainState={props.setMainState}/>
    <LogoutButton />
  </div>
}
function TransButton(props) {
  return <button onClick={() => {props.setMainState(props.state)}} id={props.state}>{props.text}</button>
}
function InternalTransactionPage(props) {
  console.log(props.currentAcc)
  console.log(props.currentData)
  return <div id='internal-page'>
    <h1>Internal</h1>
    <BackToHomeButton setMainState={props.setMainState}/>
    <LogoutButton />

  </div>
}
function ExternalTransactionPage(props) {
  console.log(props.currentAcc)
  console.log(props.currentData)
  return <div id='external-page'>
    <h1>External</h1>
    <BackToHomeButton setMainState={props.setMainState}/>
    <LogoutButton />

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
      <button id="credit" onClick={()=>{props.setCurrentAccount('credit');props.setMainState('transaction')}} ><div className="account-details" >Credit  <span >debt:{props.credit[3]}</span></div></button>
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
