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
    result = db.child('PERSONS').child(id).child('TYPE').get().val()
    if(result != 1):
        return True
    else:
        return False

# return all sections available in a list
def sections():
    result = db.child('SECTION').order_by_key().get()
    for x in result.val():
        sectionsList.append(str(x))

#retorna el horario de la seccion
def horarioClase(section):
    try:
        result = OrderedDict(db.child('SECTION').child(section).child('DAYS').child(time.currentDateName()).get().val())
        incio = str(result.values()[0])
        fin = str(result.values()[1])
        return incio, fin
    except ValueError:
        print "NO EXISTE CLASES HOY"

# retorna una lista de las secciones de hoy (se va a llamar una vez)
def sectionsOfToday():
    today = time.currentDateName().upper()
    global secHoy
    try:

        for section in sectionsList:
            result = db.child('SECTION').child(section).child('DAYS').get().val()
            for day in result:
                if(str(day) == today):
                    arreglo = [str(section), horarioClase(section)]
                    secHoy.append(arreglo)
            secHoy = sorted(secHoy, key=lambda sect: sect[1][0]) # organiza las secciones por la hora de inicio
    except ValueError:
        print "NO HAY SECCION PARA HOY"


# valida si el estudiante ya tiene hora de entrada o de salida
def validarHistoria(id):

    nombre = OrderedDict(db.child('PERSONS').child(id).get().val()).values()[4] + ' ' + OrderedDict(db.child('PERSONS').child(id).get().val()).values()[0]
    if(isProfessor(id)):
        hora_llegada = (db.child('RECORDS').child('S1').child(time.currentDate()).child('TEACHER').child(id).child('ARRIVE').get().val())

        hora_salida = (db.child('RECORDS').child('S1').child(time.currentDate()).child('TEACHER').child(id).child('LEFT').get().val())

        if (hora_llegada != None):
            lapso_time = convertTimetoDecimal(hora_llegada) + 3600 # le suma 1 hora a la llegada del profesor

        if (hora_llegada == None) & (hora_salida == None):
            db.child('RECORDS').child('S1').child(time.currentDate()).child('TEACHER').child(id).child('ARRIVE').set(time.currentTime())
            return "Bienvenid@ " + nombre # aqui va a printear en la LCD RPI

        elif (hora_salida == None) & (lapso_time <= convertTimetoDecimal(time.currentTime())):
            db.child('RECORDS').child('S1').child(time.currentDate()).child('TEACHER').child(id).child('LEFT').set(time.currentTime())
        else:
            return "Aun no puedes irte" # aqui va a printear en la LCD RPI

    else:
        hora_llegada = (db.child('RECORDS').child('S1').child(time.currentDate()).child('STUDENT').child(id).child(
            'ARRIVE').get().val())

        hora_salida = (
            db.child('RECORDS').child('S1').child(time.currentDate()).child('STUDENT').child(id).child(
                'LEFT').get().val())

        if(hora_llegada != None):
            lapso_time = convertTimetoDecimal(hora_llegada) + 1800 # le suma 30 mins a la llegada del estudiante

        if(hora_llegada == None) & (hora_salida == None):
            db.child('RECORDS').child('S1').child(time.currentDate()).child('STUDENT').child(id).child('ARRIVE').set(time.currentTime())
            return "Bienvenid@ " + nombre # aqui va a printear en la LCD RPI

        elif(hora_salida == None) & (lapso_time <= convertTimetoDecimal(time.currentTime())):
            db.child('RECORDS').child('S1').child(time.currentDate()).child('STUDENT').child(id).child('LEFT').set(time.currentTime())

        else:
            return "Aun no puedes irte" # aqui va a printear en la LCD RPI



def listar():
        sections()
        sectionsOfToday()



# convierte de hora a decimal
def convertTimetoDecimal(t):
    (h,m,s) = t.split(':')
    result = int(h) * 3600 + int(m) * 60 + int(s)
    return result

def nextClass():
    listar()
    last = secHoy[0]
    secHoy.remove(last)
    CurrentSection = secHoy[0]
    currentClass()

def currentClass():
    inicio_clase = convertTimetoDecimal(secHoy[0][1][0])
    fin_clase = convertTimetoDecimal(secHoy[0][1][1])
    hora_actual = convertTimetoDecimal(time.currentTime())
    if(hora_actual >= inicio_clase) & (hora_actual < fin_clase):
        CurrentSection = secHoy[0][0]
        return CurrentSection
    elif (len(secHoy) > 1):
        nextClass()
    else:
        return 'NO HAY MAS SECCIONES POR HOY'


