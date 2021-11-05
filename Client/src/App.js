import logo from './logo.png';
import './App.css';
import React from 'react';

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
  return <div id="login-page">
  <img style={{width:'300px', maxHeight:"50%"}} src={logo} id="logo" alt='logo'/>
  <h1 id="welcome">Welcome, Please Login</h1><div id="LoginANDRegister">
  <form id="loginForm"><p><label htmlFor="account">Account:</label><input type="text" id="account"></input></p><p><label htmlFor="password">Password:</label> <input type="password" id="password"></input></p>
      <button id="pw_login">Login with password</button></form><button id="face_login" onClick={props.onClick}>Login with FaceID</button><button id="register-button">Register</button>
      <button id="record_face" style={{display: "none"}} >Register your face</button>
      <video width="320" height="240" id="video" autoPlay={true} playsInline={true} style={{display: "none"}}></video>
  </div>
</div>
}

export default App;
