import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import pyjokes
import locale
from datetime import date

listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
joke = pyjokes.get_joke(language='es', category='neutral')
engine.setProperty('voice', 'spanish')
locale.setlocale(locale.LC_TIME, 'es_ES')
wikipedia.set_lang("es")

def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    commands = ""
    try:
        with sr.Microphone() as source:
            print('Escuchando...')
            voice = listener.listen(source)
            commands = listener.recognize_google(voice, language='es-CO')
            commands = commands.lower()
            if 'génesis' in commands:
                commands = commands.replace('génesis', '')
                print(commands)
    except:
        pass
    return commands


def run_genesis():
    commands = take_command()
    print(commands)

    if 'reproduce' in commands:
        song = commands.replace('play', '')
        talk('Ok, voy a reproducir ' + song + 'en youtube')
        pywhatkit.playonyt(song)
    
    elif 'Hola Génesis' or 'Hola Genesis':
        talk('Hola, Daniel')

    
    elif 'como estas' or 'cómo estas':
        talk('Muy superior gracias a Dios, y usted Señor?')
    


    elif 'Saluda a los profesores, y directivos' or 'saluda a los profesores y directivos':
        talk('hola, mi nombre es Jarvis, soy un modelo de inteligencia artificial creado por Daniel, estoy bastante feliz por conocerles')
    

    elif 'Gracias genesis, hasta luego' or 'gracias génesis, hasta luego':
        talk('No hay de qué, nos vemos en la próxima, un gusto conocer a tus profesores.')


    elif 'hora' in commands:
        time = datetime.datetime.now().strftime('%I:%M %p')
        talk('La hora es' + time)

    elif 'fecha' in commands:
        fecha = datetime.datetime.now().strftime('%A, %B %d, %Y')
        talk('Hoy estamos: ' + fecha)

    elif 'soltera' in commands:
        talk('No, tengo una relación seria con  el procesador jeje')

        
    elif 'gracioso' in commands:
        talk(joke)

    elif 'quien es' or 'quién es' in commands:
        person = commands.replace('Quien es ', '')
        info = wikipedia.summary(person, 1)
        print(info)
        talk(info)

    else:
        talk('No comprendo, repítelo por favor, el margen de error que tengo es alto, Daniel solo me creó para algunas funciones específicas, y los parámetros con los que me han hecho son pocos, pero creánme que está encantado de mostrarle lo increíble que puede ser la inteligencia artificial.')


while True:
    run_genesis()