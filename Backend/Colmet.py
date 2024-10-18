import speech_recognition as sr
import pyttsx3
import pywhatkit
import datetime
import wikipedia
import webbrowser
import pybible as pb
import os
import pyjokes
import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
#Configuración de voz
recognizer = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[0].id)
wikipedia.set_lang("es")

#nombre del asistente
nombre_asistente = "Colmet"

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
    hablar= ("Hola, cómo estás?")

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
        return "buenos días, cómo están?, yo estoy muy superior gracias a Dios, y ustedes?; Mucho gusto,  mi nombre es colmet, una Inteligencia artificial creada por Daniel"
    elif 12 <= hora<18:
        return "buenas tardes, cómo están?, yo estoy muy superior gracias a Dios, y ustedes?;Mucho gusto, mi nombre es colmet, una Inteligencia artificial creada por Daniel"
    else:
        return "Buenas noches, cómo están?, yo estoy muy superior gracias a Dios, y ustedes?;Mucho gusto, mi nombre es colmet, una Inteligencia artificial creada por Daniel"
def quien_es(person):
    try:
        info = wikipedia.summary(person, 1)
        hablar(f"Según Wikipedia, {person} es {info}")
        print(info)
    except wikipedia.exceptions.DisambiguationError as e:
        hablar(f"Lo siento, hay varias personas con el nombre de {person}. Puedes ser más específico?")
    except wikipedia.exceptions.PageError:
        hablar(f"Lo siento, no encontré información sobre {person} en Wikipedia.")

def subir_volumen():
    engine.setProperty('volume', engine.getProperty('volume') + 1)
    hablar("Volumen subido")

def bajar_volumen():
    engine.setProperty('volume', engine.getProperty('volume') - 1)
    hablar("Volumen bajado")
#buscar en la web
def buscar_en_google(busqueda):
    url = f"https://www.google.com/search?q={busqueda}"
    webbrowser.open(url)
# abrir redes y apps
def abrir_youtube():
    webbrowser.open('https://www.youtube.com')
def abrir_facebook():
    webbrowser.open('https://www.facebook.com')
def abrir_discord():
    webbrowser.open('https://discord.com')
def abrir_whatsapp():
    webbrowser.open('https://web.whatsapp.com')
def abrir_instagram():
    webbrowser.open('https://www.instagram.com')
def abrir_spotify():
    url = 'https://www.spotify.com'
    webbrowser.open(url)
def abrir_tiktok():
    webbrowser.open('https://www.tiktok.com')
def abrir_aplicacion(aplicacion):
    try:
        os.startfile(aplicacion)
        hablar(f"Abriendo {aplicacion}")
    except FileNotFoundError:
        hablar(f"Lo siento, no encontré la aplicación {aplicacion}")
#decir bromas
def contar_broma():
    joke = pyjokes.get_joke(language='es')
    hablar(joke)
    print(joke)
#búsqueda de versículos, y libros de la bilbia (aún se está trabajando)
def buscar_versiculo(libro, capitulo, versiculo, traduccion):
    if traduccion == 'RV1960':
        bible = pb.Bible('RV1960')
    elif traduccion == 'NTV':
        bible = pb.Bible('NTV')
    elif traduccion == 'NIV':
        bible = pb.Bible('NIV')
    elif traduccion == 'LBLA':
        bible = pb.Bible('LBLA')
    else:
        hablar("Lo siento, no tengo esa traducción disponible")
        return

    try:
        verse = bible.get_verse(libro, capitulo, versiculo)
        hablar(f"El versículo {versiculo} del capítulo {capitulo} del libro de {libro} dice: {verse}")
    except pb.VersicleNotFoundError:
        hablar(f"Lo siento, no encontré el versículo {versiculo} del capítulo {capitulo} del libro de {libro}")
def buscar_libro(libro, traduccion):
    if traduccion == 'RV1960':
        bible = pb.Bible('RV1960')
    elif traduccion == 'NTV':
        bible = pb.Bible('NTV')
    else:
        hablar("Lo siento, no tengo esa traducción disponible")
        return

    try:
        book = bible.get_book(libro)
        hablar(f"El libro de {libro} tiene {len(book)} capítulos")
    except pb.BookNotFoundError:
        hablar(f"Lo siento, no encontré el libro de {libro}")

#graficar funciones, mapas, cosas relacionadas a física
def graficar_funcion(funcion, rango):
    x = np.linspace(rango[0], rango[1], 100)
    y = eval(funcion)
    plt.plot(x, y)
    plt.title(f'Gráfico de {funcion}')
    plt.xlabel('x')
    plt.ylabel('f(x)')
    plt.grid()
    plt.show()

def simular_movimiento(gravedad=9.81, tiempo=5):
    t = np.linspace(0, tiempo, num=100)
    h = (gravedad / 2) * t**2  # h = (1/2) * g * t^2
    plt.plot(t, h)
    plt.title('Simulación de Movimiento bajo Gravedad')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Altura (m)')
    plt.grid()
    plt.show()

def crear_mapa_calor(datos):
    sns.heatmap(datos, cmap='viridis')
    plt.title('Mapa de Calor')
    plt.show()
#graficar sistema binario
def graficar_sistema_binario(duracion, intervalo):
    tiempo = np.arange(0, duracion, 0.1)  # Tiempo de 0 a 'duracion' con pasos de 0.1 segundos
    estado = []

    for t in tiempo:
        if (t // intervalo) % 2 == 0:
            estado.append(1)  # Estado encendido
        else:
            estado.append(0)  # Estado apagado

    plt.step(tiempo, estado, where='post', label='Estado del Sistema Binario')
    plt.title('Comportamiento del Sistema Binario')
    plt.xlabel('Tiempo (s)')
    plt.ylabel('Estado')
    plt.yticks([0, 1], ['Apagado', 'Encendido'])
    plt.grid()
    plt.legend()
    plt.show()


#Convertir unidades
def convertir_unidad(valor, unidad_origen, unidad_destino):
    conversiones = {
        'metros a pies': valor * 3.28084,
        'pies a metros': valor / 3.28084,
        'kilómetros a millas': valor * 0.621371,
        'millas a kilómetros': valor / 0.621371,
        'grados Celsius a grados Fahrenheit': (valor * 9/5) + 32,
        'grados Fahrenheit a grados Celsius': (valor - 32) * 5/9,
    }
    
    clave = f"{unidad_origen} a {unidad_destino}"
    if clave in conversiones:
        return conversiones[clave]
    else:
        return None


def despedirse():
    hablar(f"Hasta luego Señor, tenga un buen día, un gusto conocer a sus compañeros")

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
    hablar(f"Mucho gusto cómo están Colmetristas.{nombre_usuario.capitalize()}")


while True:


    comando = escuchar_comando()


    if nombre_asistente.lower() in comando:

        hablar("¿En qué puedo ayudarte?")
    
    elif 'busca' in comando or 'buscar' in comando:
        busqueda = comando.replace('busca', '').replace('buscar', '').strip()
        hablar(f"Buscando {busqueda} en Google...")
        buscar_en_google(busqueda)

    elif 'quién es' in comando or 'quien es' in comando:
        person = comando.replace('quién es ', '').replace('quien es ', '')
        quien_es(person)

    elif 'abre youtube' in comando or 'abrir youtube' in comando:
        abrir_youtube()
        hablar("abriendo youtube")
        hablar(f"¿En qué más puedo ayudar?,{nombre_usuario.capitalize()}?")

    elif 'abre facebook' in comando or 'abrir facebook' in comando:
        abrir_facebook()
        hablar("abriendo facebook")
        hablar(f"¿En qué más puedo ayudar?,{nombre_usuario.capitalize()}?")

    elif 'abre discord' in comando or 'abrir discord' in comando:
        abrir_discord()
        hablar("abriendo discord")
        hablar(f"¿En qué más puedo ayudar?,{nombre_usuario.capitalize()}?")

    elif 'abre whatsapp' in comando or 'abrir whatsapp' in comando:
        abrir_whatsapp()
        hablar("abriendo whastapp")
        hablar(f"¿En qué más puedo ayudar?, {nombre_usuario.capitalize()}?")
    
    elif 'abre instagram' in comando or 'abrir instagram' in comando:
        abrir_instagram()
        hablar("abriendo instagram")
        hablar(f"¿En qué más puedo ayudar?, {nombre_usuario.capitalize()}?")

    elif 'abre spotify' in comando or 'abrir spotify' in comando:
        abrir_spotify()
        hablar("abriendo spotify")
        hablar(f"¿En qué más puedo ayudar?, {nombre_usuario.capitalize()}?")
    elif 'abre tik tok' in comando or 'abrir tik tok' in comando:
        abrir_tiktok()
        hablar("abriendo tik tok")
        hablar(f"¿En qué más puedo ayudar?, {nombre_usuario.capitalize()}?")
    elif 'abre' in comando or 'abrir' in comando:
        aplicacion = comando.replace('abre', '').replace('abrir', '').strip()
        abrir_aplicacion(aplicacion)
        
#reproducir música
    elif 'reproduce' in comando:
        busqueda = comando.replace('reproduce', '')
        hablar("Reproduciendo en youtube "+busqueda)
        pywhatkit.playonyt(busqueda)
        hablar(f"¿En qué más puedo ayudar?,{nombre_usuario.capitalize()}?")
#dar la hora
    elif'hora' in comando:
        hora_actual = obtener_hora_actual()
        hablar(f"la hora actual es{hora_actual}")
    

    elif 'sube el volumen' in comando or 'subir volumen' in comando:
        subir_volumen()

    elif 'baja el volumen' in comando or 'bajar volumen' in comando:
        bajar_volumen()

    #versículos y libros para la biblia    
    elif 'qué dice el versículo' in comando or 'que dice el versículo' in comando:
        libro, capitulo, versiculo, traduccion = comando.replace('qué dice el versículo', 'que dice el versículo' '').split()
        buscar_versiculo(libro, capitulo, versiculo, traduccion)

    elif 'busca libro' in comando:
        libro, traduccion = comando.replace('buscar libro', '').split()
        buscar_libro(libro, traduccion)

    #bromas
    elif 'cuéntame una broma' in comando or 'dime una broma' in comando:
        contar_broma()

    #gráficas, funciones, mapas de calor
    elif 'crea una función' in comando:
        hablar('graficando función')
        funcion = comando.replace('grafica una función', '').strip()
        rango = [-10, 10]  # Puedes ajustar el rango según sea necesario
        graficar_funcion(funcion, rango)
        hablar('en qué más le puedo ayudar')
    
    elif 'simula movimiento' in comando:
        hablar('Creando simulación')
        simular_movimiento()
    elif 'crea un mapa de calor' in comando:
        hablar('creando un mapa de calor')
        datos = np.random.rand(10, 10)  # Genera una matriz de 10x10 con datos aleatorios
        crear_mapa_calor(datos)
        hablar('en qué más puedo ayudar?')
    elif 'grafica el sistema binario' in comando or 'graficar sistema binario' in comando:
        # Puedes preguntar por duración e intervalo o usar valores predeterminados
        hablar("¿Cuál es la duración de la simulación en segundos?")
        duracion = float(escuchar_comando())
        
        hablar("¿Cuál es el intervalo en segundos?")
        intervalo = float(escuchar_comando())
        
        graficar_sistema_binario(duracion, intervalo)
        hablar("He graficado el sistema binario. ¿En qué más puedo ayudar?")

        
    # Aquí puedes definir cómo el usuario ingresará los datos para el mapa de calor
    # Por ejemplo, podrías pedirle que hable una matriz de datos o cargar un archivo
    # Para simplificar, aquí hay un ejemplo de datos aleatorios
    elif 'convierte' in comando:
        partes = comando.replace('convierte', '').strip().split(' a ')
        valor, unidad_origen = partes[0].strip().split()
        unidad_destino = partes[1].strip()
        valor = float(valor)
        resultado = convertir_unidad(valor, unidad_origen, unidad_destino)
        if resultado is not None:
            hablar(f"{valor} {unidad_origen} son {resultado} {unidad_destino}.")
        else:
            hablar("Lo siento, no puedo realizar esa conversión.")
    #despedidas
    elif 'gracias, adiós' in comando or 'hasta luego' in comando or 'chau' in comando:
        despedirse()
        break
    else:
        hablar("no entendí tu petición, ¿puedes repetir?, el margen de error que tengo es alto, Daniel solo me creó para algunas funciones específicas, y los parámetros con los que me han hecho son pocos.")
# en caso dado no entienda la petición