# WebGUI

## Build
### Windows

Inside Anaconda or just the system environment with Visual Studio. It should be eaiser to install in WSL.
```
python -m pip install -r requirements.txt
```
## Run
``` 
python server.py
```
Then open http://localhost:8080 in browser

## TO-DO List
- [x] Login Page
- [ ] Show camera video when using face id to login
- [x] Redirect/Change to Home Page after the face of the user is recorgnised
- [x] Register Page
- [ ] Show loading animation instead of camera capture when the server is training model
- [x] Turn off camera after capturing enough photos to train model in the server
- [x] Check for the existence of username and insert new user into the DB
- [x] Redirect/Change to the Home Page after the model is trained
- [x] Home Page
- [ ] Transaction Page
- [ ] total_spend

## Some Screenshots and Explanations
Get the name of the user

![image](https://user-images.githubusercontent.com/61381909/136926481-028be9be-5004-4b5d-84e4-c09a426d9e41.png)

This page is mainly from the sample code, I just delete some unnessary parts

![image](https://user-images.githubusercontent.com/61381909/136927795-ccfa1484-4f07-4074-ad39-59d6712862ad.png)


When the user click start, the browser will start to create a peer connection with the server, then create a data channel and access the camera. The data channel will send the name of the user immediately after the channel is created, and the video track of the camera will be sent to the server through a track.

The name of the user arrive after the initialization of the `local_video`, which is a object of the class of `VideoTransformTrack` and is to handle the received frame from the browser. If the user name has not been set, the server will turn the received frame to gray and return to the browser, otherwise it will return the original received frame to the browser. The frame returned from the server will be shown under `Media`.

![image](https://user-images.githubusercontent.com/61381909/136927884-ba680a42-7271-4e48-bce9-981573dfcf7f.png)

After the user name is got by the server, a folder with the name of the user will be created inside the folder `data`.

![image](https://user-images.githubusercontent.com/61381909/136929405-460a2f18-a1c4-4277-bd57-e025a9fb6ddb.png)

And the server will save the frame into files in the user's folder.

![image](https://user-images.githubusercontent.com/61381909/136929580-e1082493-f81f-46d7-bdd5-b5c2183f5ab2.png)


