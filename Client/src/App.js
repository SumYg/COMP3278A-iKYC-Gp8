import logo from './logo.png';
import './App.css';
import React from 'react';
import {RTC2server} from "./RTCserver_connection.js"

class App extends React.Component {
  constructor(props) {
    super(props)
    this.test = this.test.bind(this)
    this.state = {
      pageState: 'login'
    }
  }
  test() {
    fetch('http://localhost:8080/test').then( response => {
      if (response.status === 200) {
        response.json().then( res => {
          // console.log("check result",res)
          console.log(res)
          this.setState({pageState: 'home'})
          // if (res.loginStatus === false) {
          //   // this.setState({pageState: 'login'})
          //   return false
          // }
          // else if (res.loginStatus === true) {
          //   // this.setState({pageState: 'logout', id: res['userID'], username: res['username']})
          //   // console.log(this.state)
          //   return true
          // }
          // console.log(x)
        })
      } else {
            // this.setState({pageState: 'login'})
            return false //error
      }
    })
  }
  render() {
    const pageState = this.state.pageState
    let body
    switch(pageState) {
      case 'login':
        body = <LoginPage onClick={this.test}/>
        break
      case 'home':
        body = <HomePage />
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

function HomePage(props) {
  return   <div id='home-page'>
    <h1>Welcome</h1>
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
    var account = document.getElementById("account").value
    let password = document.getElementById('password').value
    // alert(account)
    if (account === "" || password === "") {
      alert("Please input both the account and password")
      return
    }
    document.getElementById("record_face").style.display="none";
    document.getElementById("video").style.display="block";
    console.log(account)
    RTC2server(account, true)
  }
  function login() {
    alert("loging")
    RTC2server(null, false)
  }
  function passwordlogin(e) {
    e.preventDefault()
    props.onClick()
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
