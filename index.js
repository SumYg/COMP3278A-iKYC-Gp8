import {RTC2server} from "./RTCserver_connection.js"

document.getElementById("register-button").addEventListener("click",()=>{
    document.getElementById("pw_login").style.display="none";
    document.getElementById("face_login").style.display="none";
    document.getElementById("register-button").style.display="none";
    document.getElementById("welcome").innerText="Please register";
    document.getElementById("record_face").style.display="block";
    
  })
document.getElementById("record_face").addEventListener("click",()=>{
  var account = document.getElementById("account").value
  let password = document.getElementById('password').value
  // alert(account)
  if (account == "" || password == "") {
    alert("Please input both the account and password")
    return
  }
  document.getElementById("record_face").style.display="none";
  document.getElementById("video").style.display="block";
  console.log(account)
  RTC2server(account, true)
  // skipped stop button
})

document.getElementById('face_login').addEventListener("click", () => {
  alert("loging")
  RTC2server(null, false)
})
