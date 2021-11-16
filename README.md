# COMP3278A Group 8

## Build
1. To run this project, please install python and Node.js(https://nodejs.org/en/) first
2. all required python package can be installed by running the below command
```
python -m pip install -r requirements.txt
```
If there is error when installing one of the package in pip, you may need to install Visual C++ in [Visual Studio](https://visualstudio.microsoft.com/) first
![image](https://user-images.githubusercontent.com/61381909/142033158-60c785f4-184b-4de6-b582-78f0f8b8df4d.png)

### Connect to the database
3. As we use sophia.cs.hku.hk as the host, to connect the database, please connect to the HKUVPN first (https://www.its.hku.hk/documentation/guide/network/remote/hkuvpn2fa/windows)
### Import database
3. Or you can change the code in sqls.py (mysql.connector.connect(), in line 5-10) in order to use another host e.g. localhost:3356. You can import the table and record to your database by using the mysql command
```
# import from sql file
mysql> source h3566726.sql
```
### Running Backend Server
4. start the backend server
``` 
python server.py
```
after starting the server suvessfully, you will see the following output
![image](https://user-images.githubusercontent.com/62173795/142026369-90dc7f6c-53cc-4103-96b0-8cb55fc2191f.png)
### Running React App
5. go to the directory of the Client folder and start the react app
```
COMP3278A-iKYC-Gp8-main> cd Client
Client> npm start
```
after starting the React App sucessfully, you will see the following output and the browser will automatically goto localhost:3000![image](https://user-images.githubusercontent.com/62173795/142026839-01d50af4-8472-4df0-aa53-34b894bf583f.png)<br>
if you see the error message "'react-scripts' is not recognized as an internal or external command" when starting the React App, you mau run the below command
```
npm install
```
## IKYC System
after starting the backend server and React App, you can goto localhost:3000 start using our IKYC system
![image](https://user-images.githubusercontent.com/62173795/142028359-28befa67-499f-4b4f-99b3-e07c229bfb5b.png)
### Register an account
click the register button, input your unique username and your password, then click the button "Register your face" for registering your faceID. After clicked the button "Register your face", your device will try to open your camera and capture your face for training. Aftering training your face, you will automatically login the system<br>
![image](https://user-images.githubusercontent.com/62173795/142029999-c8ad6156-15e4-4759-9fa0-a0aeb0ebf706.png) ![image](https://user-images.githubusercontent.com/62173795/142030205-4842a44e-1d4a-47a3-b832-516a994a9e13.png)
### Demo
demo video:
https://moodle.hku.hk/course/view.php?id=86240

## Features
- [x] Login Page
<!-- - [ ] Show camera video when using face id to login -->
- [x] Redirect/Change to Home Page after the face of the user is recorgnised
- [x] Register Page
- [x] Show loading animation instead of camera capture when the server is training model
- [x] Turn off camera after capturing enough photos to train model in the server
- [x] Check for the existence of username and insert new user into the DB
- [x] Redirect/Change to the Home Page after the model is trained
- [X] Can login via both faceID or (username and password)
- [x] Home Page
- [x] Transaction Page
- [x] Stock Page
- [X]  
- [X] Can do transaction to other users' saving account (External Transaction)
- [X] Can do transaction to same user's other account (Internal Transaction)
- [X] Can search the transaction history by different selection
- [x] total_spend
