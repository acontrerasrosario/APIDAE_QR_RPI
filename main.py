import pyrebase
import datetime
"importing somethign"


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

data = {
    "Name": "Mortimer 'Morty' Smith"
}


results = db.child("Users").push(datetime.time())
print 'DONE'