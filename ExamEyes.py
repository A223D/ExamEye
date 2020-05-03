import cv2 ## For eye detection
import time ## For time outs, breaks etc.
import pyttsx3 ## For voice commands
import ctypes ## Need this for popups
import wget ##Need for downloading
import requests as req ##Need to access reset script for web interface


# create a new cam object
cap = cv2.VideoCapture(0)

face_cascade = cv2.CascadeClassifier('./haarcascade_eye.xml')
face_cascade_glasses = cv2.CascadeClassifier('./haarcascade_eye_tree_eyeglasses.xml')

## Code for initializing the voice commands
converter = pyttsx3.init()
converter.setProperty('rate', 150)
converter.setProperty('volume', 100)
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0" ## Works only in windows, will need different id for mac/linux
converter.setProperty('voice', voice_id)

start_time = time.time()

while True:
    found = 0
    end_time = time.time()
    # read the image from the cam
    _, image = cap.read()
    # converting to grayscale
    image_gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # detect all the faces in the image
    eyes = face_cascade.detectMultiScale(image_gray, 1.3, 5)
    eyes_with_glasses = face_cascade_glasses.detectMultiScale(image_gray, 1.3, 5)

    ## Detects if student is still there or not
    if len(eyes) > 0 or len(eyes_with_glasses) > 0:
        found = 1
        start_time = time.time()

    ## Generates popups if student not detected
    if (found == 0 and end_time - start_time > 5):
        ctypes.windll.user32.MessageBoxW(0, "Please focus on the test", "Surveillance ALERT", 1)
        converter.say("Please focus on test")
        converter.runAndWait()
        found = 1

    ## Drawing rectangles around the detected eyes
    if len(eyes) > 0:
        for x, y, width, height in eyes:
            cv2.rectangle(image, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)
    elif len(eyes_with_glasses) > 0:
        for x, y, width, height in eyes_with_glasses:
            cv2.rectangle(image, (x, y), (x + width, y + height), color=(255, 0, 0), thickness=2)
    else:
        pass

    ## For exiting the program
    cv2.imshow("image", image)
    if cv2.waitKey(1) == ord("q"):
        break

    url = "http://exameye.000webhostapp.com/time.txt"

    wget.download(url, './time.txt')
    f = open("time.txt", "r")
    t=f.readline()


    ## For breaks, we can customize this later
    if t>0:
        converter.say("Entering break mode")
        converter.runAndWait()
        start = time.time()
        end = time.time()
        while(end - start < (t*60)):
            end = time.time()
            resp = req.get("http://exameye.000webhostapp.com/reset.php")
        converter.say("Resuming surveillance")
        converter.runAndWait()

cap.release()
cv2.destroyAllWindows()
