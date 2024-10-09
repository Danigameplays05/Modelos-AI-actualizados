import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import time
import os

# Configuraci�n de voz
recognizer = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)  # Configuraci�n de voz inicial (masculina)

# Nombre del asistente y archivo para almacenar el nombre del usuario
nombre_asistente = "Jarvis"
archivo_nombre = "nombre_usuario.txt"
recordatorios = []

# Funci�n para hablar
def hablar(texto):
    engine.say(texto)
    engine.runAndWait()

# Obtener nombre del usuario
def obtener_nombre_usuario():
    try:
        with open(archivo_nombre, 'r') as file:
            nombre = file.read().strip()
            if nombre:
                return nombre.lower()
    except FileNotFoundError:
        pass
    return None

# Establecer nombre del usuario
def establecer_nombre_usuario():
    hablar("Hola, �c�mo te llamas?")
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            nombre = recognizer.recognize_google(audio, language='es-CO')
            with open(archivo_nombre, 'w') as file:
                file.write(nombre.lower())
            return nombre.lower()
        except sr.WaitTimeoutError:
            hablar("Parece que tardaste en responder, intentemos de nuevo.")
            return ""
        except sr.UnknownValueError:
            hablar("No pude entenderte, �puedes repetir tu nombre?")
            return ""

# Obtener la hora actual
def obtener_hora_actual():
    return datetime.datetime.now().strftime('%H:%M:%S')

# Obtener la fecha actual
def obtener_fecha_actual():
    return datetime.datetime.now().strftime('%d/%m/%Y')

# Obtener saludo basado en la hora del d�a
def obtener_saludo():
    hora = datetime.datetime.now().hour
    if 5 <= hora < 12:
        return "Buenos d�as"
    elif 12 <= hora < 18:
        return "Buenas tardes"
    else:
        return "Buenas noches"

# Escuchar comando
def escuchar_comando():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source, duration=1)
        try:
            print("Te escucho...")
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            texto = recognizer.recognize_google(audio, language='es')
            return texto.lower()
        except sr.WaitTimeoutError:
            return ""
        except sr.UnknownValueError:
            return ""

# Buscar en Wikipedia
def buscar_en_wikipedia(consulta):
    wikipedia.set_lang("es")
    resultado = wikipedia.summary(consulta, sentences=2)
    hablar(f"Esto es lo que encontr� sobre {consulta}: {resultado}")

# A�adir un recordatorio
def añadir_recordatorio(recordatorio):
    recordatorios.append(recordatorio)
    hablar(f"Recordatorio añadido: {recordatorio}")

# Ver recordatorios
def ver_recordatorios():
    if recordatorios:
        hablar("Tienes los siguientes recordatorios:")
        for i, rec in enumerate(recordatorios, 1):
            hablar(f"{i}. {rec}")
    else:
        hablar("No tienes recordatorios pendientes.")

# Ajustar la voz del asistente
def cambiar_voz(tipo_voz):
    if tipo_voz == 'masculina':
        engine.setProperty('voice', voices[0].id)
        hablar("Voz cambiada a masculina.")
    elif tipo_voz == 'femenina':
        engine.setProperty('voice', voices[1].id)
        hablar("Voz cambiada a femenina.")
    else:
        hablar("Lo siento, no reconozco ese tipo de voz.")

# Funci�n principal del asistente
def iniciar_asistente():
    nombre_usuario = obtener_nombre_usuario()
    if not nombre_usuario:
        nombre_usuario = establecer_nombre_usuario()
    
    if nombre_usuario:
        saludo = obtener_saludo()
        hora_actual = obtener_hora_actual()
        hablar(f"{saludo}, {nombre_usuario.capitalize()}! Son las {hora_actual}. �En qu� puedo servirte?")

    while True:
        comando = escuchar_comando()

        if nombre_asistente.lower() in comando:
            hablar("�En qu� puedo ayudarte?")
        
        elif 'hora' in comando:
            hora_actual = obtener_hora_actual()
            hablar(f"La hora actual es {hora_actual}.")

        elif 'fecha' in comando:
            fecha_actual = obtener_fecha_actual()
            hablar(f"Hoy es {fecha_actual}.")

        elif 'reproduce' in comando:
            busqueda = comando.replace('reproduce', '').strip()
            hablar(f"Reproduciendo {busqueda} en YouTube.")
            pywhatkit.playonyt(busqueda)

        elif 'buscar en wikipedia' in comando:
            consulta = comando.replace('buscar en wikipedia', '').strip()
            buscar_en_wikipedia(consulta)

        elif 'a�adir recordatorio' in comando:
            recordatorio = comando.replace('a�adir recordatorio', '').strip()
            añadir_recordatorio(recordatorio)

        elif 'ver recordatorios' in comando:
            ver_recordatorios()

        elif 'cambiar voz' in comando:
            if 'masculina' in comando:
                cambiar_voz('masculina')
            elif 'femenina' in comando:
                cambiar_voz('femenina')

        elif 'gracias' in comando and 'adi�s' in comando:
            hablar("Hasta luego, un gusto haberte conocido.")
            break

        else:
            hablar("Lo siento, no entend� tu petici�n. �Puedes repetir?")

# Iniciar el asistente
iniciar_asistente()

