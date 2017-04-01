import pyrebase
from collections import OrderedDict
import RegisterTime as time
import thread
import time as timer


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

CurrentSection = None
InitialHour = None
EndHour = None

# a list of sections available
sectionsList = []
#
secHoy = []





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

#retorna el horario de la seccion
def horarioClase(section):
    result = OrderedDict(db.child('Section').child(section).child('days').child(time.currentDateName()).get().val())
    incio = str(result.values()[0])
    fin = str(result.values()[1])
    return incio, fin

# retorna una lista de las secciones de hoy (se va a llamar una vez)
def sectionsOfToday():
    today = time.currentDateName().upper()
    global secHoy
    try:

        for section in sectionsList:
            result = db.child('Section').child(section).child('days').get().val()
            for day in result:
                if(day == today):
                    arreglo = [str(section), horarioClase(section)]
                    secHoy.append(arreglo)
            secHoy = sorted(secHoy, key=lambda sect: sect[1][0]) # organiza las secciones por la hora de inicio
    except ValueError:
        print "NO HAY SECCION PARA HOY"


def listar():
        sections()
        sectionsOfToday()
        print secHoy

# pruebas
while True:
    if (firebase == '20:34:25'):
        listar()
        timer.sleep(1)
        print secHoy


