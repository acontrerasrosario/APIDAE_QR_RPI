import pyrebase

config = {
      "apiKey": "AIzaSyB0IXn8A10yGVM5rGR871L7i2BapIOMgQQ",
      "authDomain": "apidae-4f97d.firebaseapp.com",
      "databaseURL": "https://apidae-4f97d.firebaseio.com",
      "storageBucket": "apidae-4f97d.appspot.com"
    }
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password('acontrerasrosario@gmail.com','emilio123456')
db = firebase.database()


def startconfig():

