import cv2
import numpy as np
import face_recognition
import os
import pandas as pd
from datetime import datetime

# Path to the folder containing training images
path = r"C:\Users\DELL\Desktop\Face-Recognition-Attendance-Projects-main\Training_images"
images = []
classNames = []

# Load training images
myList = os.listdir(path)
print(f"Training images: {myList}")
for cl in myList:
    curImg = cv2.imread(f'{path}/{cl}')
    images.append(curImg)
    classNames.append(os.path.splitext(cl)[0])

print(f"Class names: {classNames}")

# Function to encode faces
def findEncodings(images):
    encodeList = []
    for img in images:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        try:
            encode = face_recognition.face_encodings(img)[0]
            encodeList.append(encode)
        except IndexError:
            print("Face not detected in one of the images. Skipping...")
    return encodeList

encodeListKnown = findEncodings(images)
print('Encoding Complete')

# Attendance file setup
attendance_file = "Attendance.xlsx"
if not os.path.exists(attendance_file):
    df = pd.DataFrame(columns=["Name", "Date", "Time", "Status"])
    df.to_excel(attendance_file, index=False)

# Initialize webcam
cap = cv2.VideoCapture(0)
if not cap.isOpened():
    print("Error: Could not access the webcam.")
    exit()

attendance_log = {}

while True:
    success, img = cap.read()
    if not success:
        print("Failed to grab frame.")
        break

    # Resize and preprocess the frame
    imgS = cv2.resize(img, (0, 0), None, 0.25, 0.25)
    imgS = cv2.cvtColor(imgS, cv2.COLOR_BGR2RGB)

    # Detect and encode faces
    facesCurFrame = face_recognition.face_locations(imgS)
    encodesCurFrame = face_recognition.face_encodings(imgS, facesCurFrame)

    for encodeFace, faceLoc in zip(encodesCurFrame, facesCurFrame):
        matches = face_recognition.compare_faces(encodeListKnown, encodeFace, tolerance=0.5)
        faceDis = face_recognition.face_distance(encodeListKnown, encodeFace)
        matchIndex = np.argmin(faceDis)

        if matches[matchIndex] and faceDis[matchIndex] < 0.5:  # High accuracy check
            name = classNames[matchIndex].upper()
            current_time = datetime.now()
            date_str = current_time.strftime("%Y-%m-%d")
            time_str = current_time.strftime("%H:%M:%S")

            # Log attendance if new or after the time threshold
            if name not in attendance_log or (current_time - attendance_log[name]).seconds > 10:
                attendance_log[name] = current_time

                # Save attendance
                df = pd.read_excel(attendance_file)
                new_row = pd.DataFrame([{"Name": name, "Date": date_str, "Time": time_str, "Status": "Present"}])
                df = pd.concat([df, new_row], ignore_index=True)
                df.to_excel(attendance_file, index=False)

            # Draw bounding box and name on the face
            y1, x2, y2, x1 = faceLoc
            y1, x2, y2, x1 = y1 * 4, x2 * 4, y2 * 4, x1 * 4
            cv2.rectangle(img, (x1, y1), (x2, y2), (0, 255, 0), 2)
            cv2.rectangle(img, (x1, y2 - 35), (x2, y2), (0, 255, 0), cv2.FILLED)
            cv2.putText(img, name, (x1 + 6, y2 - 6), cv2.FONT_HERSHEY_COMPLEX, 1, (255, 255, 255), 2)

    # Display the webcam feed
    cv2.imshow('Webcam', img)

    # Exit on pressing 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
