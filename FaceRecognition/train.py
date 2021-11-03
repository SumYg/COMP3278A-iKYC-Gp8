import os
import numpy as np
from PIL import Image
import asyncio
import cv2
import pickle

recognizer = cv2.face.LBPHFaceRecognizer_create()
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
face_cascade = cv2.CascadeClassifier(os.path.join(BASE_DIR, 'haarcascade/haarcascade_frontalface_default.xml'))
labels = None
CONFIDENCE_LEVEL = 80

def initialize_face_recogn():
    global labels
    labels = {"person_name": 1}
    with open("labels.pickle", "rb") as f:
        labels = pickle.load(f)
        labels = {v: k for k, v in labels.items()}
    recognizer.read("train.yml")

async def recorgn_face(frame):
    """
        This function tries to recorgnise registered face from the frame
        Return: Frame
    """
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.5, minNeighbors=3)

    for (x, y, w, h) in faces:
        roi_gray = gray[y:y + h, x:x + w]
        roi_color = frame[y:y + h, x:x + w]
        # predict the id and confidence for faces
        id_, conf = recognizer.predict(roi_gray)

        # 3.1 If the face is recognized
        if conf >= CONFIDENCE_LEVEL:
            # print(id_)
            # print(labels[id_])
            font = cv2.QT_FONT_NORMAL
            id = 0
            id += 1
            name = labels[id_]
            print(name, x, w, y, h)
            current_name = name
            color = (255, 0, 0)
            stroke = 2
            cv2.putText(frame, name, (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))

            # # Find the customer's information in the database.
            # select = "SELECT customer_id, name, DAY(login_date), MONTH(login_date), YEAR(login_date) FROM Customer WHERE name='%s'" % (name)
            # name = cursor.execute(select)
            # result = cursor.fetchall()
            # # print(result)
            # data = "error"

            # for x in result:
            #     data = x

            # # If the customer's information is not found in the database
            # if data == "error":
            #     print("The customer", current_name, "is NOT FOUND in the database.")

            # # If the customer's information is found in the database
            # else:
            #     """
            #     Implement useful functions here.
                

            #     """
            #     # Update the data in database
            #     update =  "UPDATE Customer SET login_date=%s WHERE name=%s"
            #     val = (date, current_name)
            #     cursor.execute(update, val)
            #     update = "UPDATE Customer SET login_time=%s WHERE name=%s"
            #     val = (current_time, current_name)
            #     cursor.execute(update, val)
            #     myconn.commit()
               
            #     hello = ("Hello ", current_name, "Welcom to the iKYC System")
            #     print(hello)
            #     engine.say(hello)
            #     # engine.runAndWait()


        # 3.2 If the face is unrecognized
        else: 
            color = (255, 0, 0)
            stroke = 2
            font = cv2.QT_FONT_NORMAL
            cv2.putText(frame, "UNKNOWN", (x, y), font, 1, color, stroke, cv2.LINE_AA)
            cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), (2))
    return frame

async def train_model():
    image_dir = os.path.join(BASE_DIR, "data")

    # Load the OpenCV face recognition detector Haar
    # Create OpenCV LBPH recognizer for training

    current_id = 0
    label_ids = {}
    y_label = []
    x_train = []

    # Traverse all face images in `data` folder
    for root, dirs, files in os.walk(image_dir):
        for file in files:
            if file.endswith("png") or file.endswith("jpg"):
                path = os.path.join(root, file)
                label = os.path.basename(root).replace("", "").upper()  # name
                print(label, path)

                if label in label_ids:
                    pass
                else:
                    label_ids[label] = current_id
                    current_id += 1
                id_ = label_ids[label]
                print(label_ids)

                pil_image = Image.open(path).convert("L")
                image_array = np.array(pil_image, "uint8")
                print(image_array)
                # Using multiscle detection
                faces = face_cascade.detectMultiScale(image_array, scaleFactor=1.5, minNeighbors=3)

                for (x, y, w, h) in faces:
                    roi = image_array[y:y+h, x:x+w]
                    x_train.append(roi)
                    y_label.append(id_)

    # labels.pickle store the dict of labels.
    # {name: id}  
    # id starts from 0
    with open("labels.pickle", "wb") as f:
        pickle.dump(label_ids, f)

    # Train the recognizer and save the trained model.
    recognizer.train(x_train, np.array(y_label))
    recognizer.save("train.yml")
    print("Trained")
    print("Trained")
