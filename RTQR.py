import zbar
import datetime
from PIL import Image
import cv2
import pyrebase


config = {
  "apiKey": "TokenKey",
  "authDomain": "ProjectId.firebaseapp.com",
  "databaseURL": "https://projectID.firebaseio.com",
  "storageBucket": "projectID.appspot.com"
}

firebase = pyrebase.initialize_app(config)

auth = firebase.auth()

user = auth.sign_in_with_email_and_password('adfbdfbdfb@gmail.com','gbildgbdfdfb')

db = firebase.database()

def main():



    capture = cv2.VideoCapture(0)

    while True:
        # To quit this program press q.
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # Breaks down the video into frames
        ret, frame = capture.read()

        # Displays the current frame
        cv2.imshow('Current', frame)

        # Converts image to grayscale.
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Uses PIL to convert the grayscale image into a ndary array that ZBar can understand.
        image = Image.fromarray(gray)
        width, height = image.size
        zbar_image = zbar.Image(width, height, 'Y800', image.tobytes())

        # Scans the zbar image.
        scanner = zbar.ImageScanner()
        scanner.scan(zbar_image)

        # Prints data from image.
        for decoded in zbar_image:
            #Testing way to upload data to firebase
            db.child("historia/").child(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y")).set(decoded.data)



if __name__ == "__main__":
    main()
