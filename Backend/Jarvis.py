import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
#Configuración de voz
recognizer = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
wikipedia.set_lang("es")

#nombre del asistente


nombre_asistente = "Jarvis"

#almacenamos nuestro nombre
archivo_nombre = "nombre_usuario.txt"


def obtener_nombre_usuario():
    try:
        with open(archivo_nombre , 'r') as file:
            nombre = file.read()



            if nombre:

                return nombre
    except FileNotFoundError:

        pass

    return None


def establecer_nombre_usuario():
    hablar=("Hola, Buenas tardes, cómo estás? Daniel")

    with sr.Microphone() as source:
        #ajustamos el ruido ambiental
        recognizer.adjust_for_ambient_noise(source,duration=1)

        try:
            audio = recognizer.listen(source,timeout=5,phrase_time_limit=5)

            nombre= recognizer.recognize_google(audio,language='es-CO')

            with open(archivo_nombre,'w') as file:
                
                file.write(nombre)

            return nombre.lower()
        
        except sr.WaitTimeoutError:
            return ""
        
        except sr.UnknownValueError:
            return ""


def obtener_hora_actual():
    hora = datetime.datetime.now()

    hora = hora.strftime('%H: %M: %S')

    return hora 

def obtener_saludo():

    hora = datetime.datetime.now()

    hora = hora.hour

    if 5<= hora < 12:
        return "buenos días, cómo están?"
    elif 12 <= hora<18:
        return "buenas tardes, cómo están?, yo estoy muy superior gracias a Dios, y ustedes?"
    else:
        return "Buenas noches, cómo se encuentran?"
    
def escuchar_comando():

    with sr.Microphone() as source:
        print("Te escucho...")
        recognizer.adjust_for_ambient_noise(source,duration=1)


        try:

            audio = recognizer.listen(source,timeout=5,phrase_time_limit=5)
            
            texto = recognizer.recognize_google(audio,language='es')

            return texto.lower()
        


        except sr.WaitTimeoutError:
            return ""

        except sr.UnknownValueError:
            return ""



def hablar(texto):
    engine.say(texto)
    engine.runAndWait()
nombre_usuario = obtener_nombre_usuario()

if nombre_usuario:

    saludo = obtener_saludo()
    hora_actual = obtener_hora_actual()

    hablar(f"{saludo}, {nombre_usuario.capitalize()}!Son las {hora_actual}.¿En qué puedo servirte")
else:
    nombre_usuario = establecer_nombre_usuario()
    hablar(f"Mucho gusto cómo estás Daniel,{nombre_usuario.capitalize()}")

while True:


    comando = escuchar_comando()


    if nombre_asistente.lower() in comando:

        hablar("¿En qué puedo ayudarte?")

    elif 'reproduce' in comando:
        busqueda = comando.replace('reproduce', '')
        hablar("Reproduciendo en youtube "+busqueda)
        pywhatkit.playonyt(busqueda)

        hablar(f"¿En qué más ayudar?,{nombre_usuario.capitalize()}?")
    elif'hora' in comando:

        hora_actual = obtener_hora_actual()
        hablar(f"la hora actual es{hora_actual}")
    
    elif 'quien es' or 'quién es' in comando:
        person = comando.replace('Quien es ', '')
        info = wikipedia.summary(person, 1)
        print(info)
        hablar(info)

    elif 'Gracias Jarvis, adiós.' in comando:
        hablar("Hasta luego Señor, un gusto conocerles")

        break

    else:
        hablar("no entendí tu petición, ¿puedes repetir?, el margen de error que tengo es alto, Daniel solo me creó para algunas funciones específicas, y los parámetros con los que me han hecho son pocos, pero creánme que está encantado de mostrarle lo increíble que puede ser la inteligencia artificial.")

else:
    print("Jarvis está durmiendo")