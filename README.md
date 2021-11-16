# COMP3278A Group 8

## Build
1. To run this project, please install python and Node.js(https://nodejs.org/en/) first
2. all required python package can be installed by running the below command
```
python -m pip install -r requirements.txt
```
If error occur when installing some packages in Windows, you may need to install Visual C++ in [Visual Studio](https://visualstudio.microsoft.com/) first
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
5. open another terminal and go to the directory of the Client folder, and start the react app
```
Client> npm start
```
after starting the React App sucessfully, you will see the following output and the browser will automatically goto http://localhost:3000 ![image](https://user-images.githubusercontent.com/62173795/142026839-01d50af4-8472-4df0-aa53-34b894bf583f.png)<br>
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
### Do transaction
after clicking the account button, you can see your saving, credit and investment account. Click any one of the account, you can see the transaction page. By clicking external in Saving account, you can transfer money to the saving accounts of other people. You can transfer money within your Saving/Investmnet/Credit account by internal transaction
<br>![image](https://user-images.githubusercontent.com/62173795/142050098-d70f37d2-9e8b-444c-aa14-a62cb4198cbe.png) ![image](https://user-images.githubusercontent.com/62173795/142050339-5121e98c-6412-4a3f-b627-148a81e7e6f4.png) ![image](https://user-images.githubusercontent.com/62173795/142046734-469eeab5-ce6a-44a9-94bc-5149e4f03604.png)
### Buy/Sell stock
in the stock page, you can view different stocks. And you can buy stock by using the money in your investment account, so please transfer money to your investment account from your saving/credit account by doing internal transaction first ;)<br>
![image](https://user-images.githubusercontent.com/62173795/142047289-d05eb548-f908-4c1a-986b-fabd518604c0.png)
![image](https://user-images.githubusercontent.com/62173795/142047449-8ab170f6-8565-40cd-9f0a-01499041a74c.png)
### Searching transaction history
you can search the transaction history by different selection option 
<br>(can leave some selection option to be empty e.g. transaction with amount <$1 in time period 12/11/2021-13/11/2021)
<br>![image](https://user-images.githubusercontent.com/62173795/142049206-c6da3103-4248-4259-b0aa-dfe7d15017e4.png)




### Demo
demo video: https://drive.google.com/drive/folders/1FV2h3xu1VhOoKSIShewkzHqVLPiPJEGF
guideline for Building: https://connecthkuhk-my.sharepoint.com/personal/edmundcy_connect_hku_hk/_layouts/15/onedrive.aspx?id=%2Fpersonal%2Fedmundcy%5Fconnect%5Fhku%5Fhk%2FDocuments%2FInstallation%20demo%2Emkv&parent=%2Fpersonal%2Fedmundcy%5Fconnect%5Fhku%5Fhk%2FDocuments

## Features
- [x] Login Page
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



## Transaction Page Features
- [X] Can show the balance of different account
- [X] Can do transaction to other users' saving account (External Transaction)
- [X] Can do transaction to other users' saving account (External Transaction)
- [X] Can do transaction to same user's other account (Internal Transaction)
- [X] Can search the transaction history by different selection option (can leave some selection option to be empty, or even use all the selection option)

## Stock Page Features
- [x] Show details of all available stocks, such as stock code, current price
- [x] Can buy or sell stocks using investment account
- [x] % change: The percentage change between current price and closing price
- [x] Total spend: Total money spent on that stock
- [X] History Profit: Total amount that earned from that stock
- [X] Current Value: Current value of all owned stock
