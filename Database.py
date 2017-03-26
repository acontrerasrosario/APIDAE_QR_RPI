import pyrebase
import RegisterTime as time
config = {
      "apiKey": "AIzaSyAVJ5yBzKo2wDpm6fPtAPLmMEydVTz0GTk",
      "authDomain": "apidae-85302.firebaseapp.com",
      "databaseURL": "https://apidae-85302.firebaseio.com",
      "storageBucket": "apidae-85302.appspot.com"
    }
firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
user = auth.sign_in_with_email_and_password('acontrerasrosario@gmail.com', '123456')
db = firebase.database()

# a list of sections available
sectionsList = []

# check if is the ID is a professor
def isProfessor(id):
    result = db.child('Persons').child(id).child('type').get().val()
    if(result != 1):
        return True
    else:
        return False

# return all sections available in a list
def sections():
    result = db.child('Section').order_by_key().get()
    for x in result.val():
        sectionsList.append(x)


# returns all section of the DAY
def seccionOfToday():
    sections()
    resultado_final = None
    for xx in sectionsList:
        result = db.child('Section').child(xx).child('days').get()
        for x in result.val():
            if x == time.currentDateName().upper():
                resultado_final = db.child('Section').child(xx).get().key()
            else:
                resultado_final = 'NO HAY CLASE HOY'
    return resultado_final



