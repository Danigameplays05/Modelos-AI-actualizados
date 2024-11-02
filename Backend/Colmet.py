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
from matplotlib.animation import FuncAnimation
import seaborn as sns
from googletrans import Translator
import tkinter as tk
from tkinter import messagebox
import pygame
import math
import threading
translator = Translator()
#Configuración de voz
recognizer = sr.Recognizer()

engine = pyttsx3.init()
voices = engine.getProperty('voices')
engine.setProperty('voices', voices[1].id)
for index, voice in enumerate(voices):
    print(f"Voz {index}: {voice.name} - {voice.languages}")
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

            nombre= recognizer.recognize_google(audio,language='en-CO')

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
        return "¡Buenas tardes, cómo se están docentes y maestros?!, yo estoy muy superior gracias a Dios, y ustedes?;Mucho gusto, mi nombre es colmet, una Inteligencia artificial creada por Daniel, alguien quien tenía este proyecto desde hace mucho tiempo, pero no había podido presentarlo. Originalmente, he surgido a causa de los avances tecnológicos que se han venido presentando, por lo cual Daniel pensó en crear un modelo de inteligencia artificial o asistente virtual, que pudiese automatizar tareas. Así que"
    elif 12 <= hora<18:
        return "¡buenas tardes, cómo están?!, yo estoy muy superior gracias a Dios, y ustedes?;Mucho gusto, mi nombre es colmet, una Inteligencia artificial creada por Daniel, alguien quien tenía este proyecto desde hace mucho tiempo, pero no había podido presentarlo. Originalmente, he surgido a causa de los avances tecnológicos que se han venido presentando, por lo cual Daniel pensó en crear un modelo de inteligencia artificial o asistente virtual, que pudiese automatizar tareas. Así que"
    else:
        return "Buenas noches, cómo están?, yo estoy muy superior gracias a Dios, y ustedes?;Mucho gusto, mi nombre es colmet, una Inteligencia artificial creada por Daniel"
#buscar conceptos, personas, significados etc.
def quien_es(person):
    try:
        info = wikipedia.summary(person, 1)
        hablar(f"Según Wikipedia, {person} es {info}")
        print(info)
    except wikipedia.exceptions.DisambiguationError as e:
        hablar(f"Lo siento, hay varias personas con el nombre de {person}. Puedes ser más específico?")
    except wikipedia.exceptions.PageError:
        hablar(f"Lo siento, no encontré información sobre {person} en Wikipedia.")

def definir_concepto(concepto):
    try:
        info = wikipedia.summary(concepto, sentences=2)  # Obtener un resumen de 2 oraciones
        hablar(f"Según Wikipedia, {concepto} es {info}")
        print(info)  # Imprimir la información en la consola
    except wikipedia.exceptions.DisambiguationError as e:
        hablar(f"Lo siento, hay varias definiciones para {concepto}. Puedes ser más específico?")
    except wikipedia.exceptions.PageError:
        hablar(f"Lo siento, no encontré información sobre {concepto} en Wikipedia.")
        

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
def Experimento():

    def draw_input_box(surface, text, x, y, active):
        font = pygame.font.Font(None, 36)
        input_box = pygame.Rect(x, y, 200, 40)
        color = (255, 0, 0) if active else (100, 100, 100)
        pygame.draw.rect(surface, color, input_box, 2)
        text_surface = font.render(text, True, (255, 255, 255))
        surface.blit(text_surface, (input_box.x + 5, input_box.y + 5))
        return input_box

    # Inicializar Pygame
    pygame.init()
    width, height = 1200, 750
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Simulación de Semiparábola en el Aire")

    # Colores
    DARK_GRAY = (30, 30, 30)
    LIGHT_GRAY = (200, 200, 200)
    BLUE = (50, 150, 255)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    DARK_BLUE = (0, 0, 139)
    BUTTON_COLOR = (70, 130, 180)
    BUTTON_HOVER_COLOR = (100, 150, 200)

    # Variables iniciales
    h0 = 300  # Altura inicial
    g = 9.81   # Gravedad
    results = ''  # Variable para mostrar resultados

    # Bucle principal
    running = True
    input_v0 = ''
    input_theta = ''
    active_v0 = False
    active_theta = False

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if active_v0:
                    if event.key == pygame.K_RETURN:
                        active_v0 = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_v0 = input_v0[:-1]
                    else:
                        input_v0 += event.unicode
                if active_theta:
                    if event.key == pygame.K_RETURN:
                        active_theta = False
                    elif event.key == pygame.K_BACKSPACE:
                        input_theta = input_theta[:-1]
                    else:
                        input_theta += event.unicode
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Si se hace clic izquierdo
                    if v0_box.collidepoint(event.pos):
                        active_v0 = True
                        active_theta = False
                    elif theta_box.collidepoint(event.pos):
                        active_theta = True
                        active_v0 = False
                    else:
                        active_v0 = False
                        active_theta = False

        # Dibujar fondo y elementos
        screen.fill(DARK_GRAY)

        # Título
        font = pygame.font.Font(None, 48)
        title_surface = font.render(
            "Simulación de Semiparábola", True, LIGHT_GRAY)
        screen.blit(title_surface, (350, 20))

        # Instrucciones
        instruction_surface = font.render(
            "Ingrese Velocidad Inicial (m/s) y Ángulo (grados):", True, LIGHT_GRAY)
        screen.blit(instruction_surface, (200, 80))

        # Cuadros de entrada
        v0_box = draw_input_box(screen, input_v0, 480, 150, active_v0)
        theta_box = draw_input_box(screen, input_theta, 480, 220, active_theta)

        # Botón de inicio
        mouse_x, mouse_y = pygame.mouse.get_pos()
        button = pygame.Rect(400, 400, 350, 50)
        if button.collidepoint((mouse_x, mouse_y)):
            pygame.draw.rect(screen, BUTTON_HOVER_COLOR, button)
        else:
            pygame.draw.rect(screen, BUTTON_COLOR, button)
        button_text = font.render("Iniciar Simulación", True, LIGHT_GRAY)
        screen.blit(button_text, (button.x + 30, button.y + 10))

        # Lógica de simulación
        if event.type == pygame.MOUSEBUTTONDOWN:
            if button.collidepoint(event.pos):
                try:
                    v0 = float(input_v0)
                    theta = float(input_theta)
                    theta_rad = math.radians(theta)
                    time = 0
                    running_simulation = True
                    trajectory = []
                    x_values = []
                    y_values = []

                    # Bucle de la simulación
                    while running_simulation:
                        for sim_event in pygame.event.get():
                            if sim_event.type == pygame.QUIT:
                                running_simulation = False

                        # Lógica de movimiento
                        time += 0.1  # Incrementar tiempo en 0.1 segundos
                        x_position = v0 * math.cos(theta_rad) * time
                        y_position = h0 + (v0 * math.sin(theta_rad)
                                           * time) - (0.5 * g * (time ** 2))

                        # Detener la simulación cuando el proyectil toca el suelo
                        if y_position <= 0:
                            running_simulation = False
                            y_position = 0  # Asegurarse de que y_position no sea negativa

                        # Almacenar las posiciones para el gráfico
                        x_values.append(x_position)
                        y_values.append(y_position)

                        # Limpiar la pantalla
                        screen.fill(DARK_GRAY)

                        # Dibujar proyectil
                        if y_position >= 0:  # Solo dibujar si el proyectil está en el aire
                            pygame.draw.circle(
                                screen, BLUE, (int(x_position), int(height - y_position)), 10)
                            # Almacenar trayectoria
                            trajectory.append(
                                (int(x_position), int(height - y_position)))

                        # Dibujar la trayectoria
                        if len(trajectory) > 1:
                            # Dibujar la línea de trayectoria
                            pygame.draw.lines(
                                screen, RED, False, trajectory, 2)

                        # Mostrar resultados en pantalla
                        results = f"Tiempo total de vuelo: {time:.2f} s | Distancia horizontal: {
                            x_position:.2f} píxeles | Altura máxima: {max(y_values):.2f} píxeles"
                        result_surface = font.render(results, True, LIGHT_GRAY)
                        screen.blit(result_surface, (50, 680))

                        pygame.display.flip()
                        # Esperar un tiempo antes del siguiente frame
                        pygame.time.delay(100)

                    # Análisis del movimiento
                    total_time = time
                    horizontal_distance = x_position
                    max_height = max(y_values)

                    # Mostrar resultados en consola
                    print(f"Tiempo total de vuelo: {total_time:.2f} segundos")
                    print(f"Distancia horizontal recorrida: {
                        horizontal_distance:.2f} píxeles")
                    print(f"Altura máxima alcanzada: {max_height:.2f} píxeles")

                    # Graficar posiciones
                    plt.figure(figsize=(10, 5))

                    # Gráfico de trayectoria
                    plt.subplot(1, 2, 1)
                    plt.plot(x_values, y_values, color='blue')
                    plt.title('Trayectoria del Proyectil')
                    plt.xlabel('Distancia Horizontal (píxeles)')
                    plt.ylabel('Altura (píxeles)')
                    plt.grid()

                    # Gráfico de tiempo vs posición
                    plt.subplot(1, 2, 2)
                    time_values = [i * 0.1 for i in range(len(x_values))]
                    plt.plot(time_values, x_values,
                             label='Posición Horizontal', color='orange')
                    plt.plot(time_values, y_values,
                             label='Altura', color='green')
                    plt.title('Movimiento del Proyectil')
                    plt.xlabel('Tiempo (s)')
                    plt.ylabel('Posición (píxeles)')
                    plt.legend()
                    plt.grid()

                    plt.tight_layout()
                    plt.show()

                except ValueError:
                    print(
                        "Por favor, ingrese valores válidos para la velocidad y el ángulo.")
        # Cerrar Pygame
        pygame.display.flip()
    pygame.quit()




#graficar sistema binario
def graficar_sistema_binario(duracion, intervalo):
    tiempo = np.arange(0, duracion, 0.1)  # Tiempo de 0 a 'duracion' con pasos de 0.1 segundos
    estado = []

    # Generar el estado del sistema binario
    for t in tiempo:
        if (t // (intervalo / 2)) % 2 == 0:
            estado.append(1)  # Estado encendido
        else:
            estado.append(0)  # Estado apagado

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, duracion)
    ax.set_ylim(-0.5, 1.5)
    ax.set_title('Comportamiento del Sistema Binario', fontsize=16, fontweight='bold')
    ax.set_xlabel('Tiempo (s)', fontsize=12)
    ax.set_ylabel('Estado', fontsize=12)
    ax.set_yticks([0, 1])
    ax.set_yticklabels(['Apagado', 'Encendido'])
    ax.grid(True)

    # Inicializar la línea que representará el estado
    line, = ax.plot([], [], lw=2, color='blue')

    # Función de inicialización
    def init():
        line.set_data([], [])
        return line,

    # Función de actualización para la animación
    def update(frame):
        x_data = tiempo[:frame]
        y_data = estado[:frame]
        line.set_data(x_data, y_data)
        return line,

    # Crear la animación
    ani = FuncAnimation(fig, update, frames=len(tiempo), init_func=init, blit=True, interval=100)

    plt.title('Comportamiento del Sistema Binario', fontsize=16, fontweight='bold')
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.axvline(0, color='black', lw=0.5, ls='--')
    plt.show()


#leyes de kepler
def animar_orbita(a, b, c, d):
    # Generar puntos para la elipse
    theta = np.linspace(0, 2 * np.pi, 100)
    x1 = a * np.cos(theta)  # Eje mayor
    y1 = b * np.sin(theta)  # Eje menor
    x2 = c * np.cos(theta)  # Eje mayor
    y2 = d * np.sin(theta)  # Eje menor

    # Crear la figura y los ejes
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='lightblue')
    ax.set_xlim(-max(a, c)-1, max(a, c)+1)
    ax.set_ylim(-max(b, d)-1, max(b, d)+1)
    ax.set_aspect('equal')
    ax.grid(color='white', linestyle='--', linewidth=0.5)  # Cuadrícula más sutil
    ax.set_title('Movimiento de Planetas en Órbita Elíptica', fontsize=16, fontweight='bold')
    ax.set_xlabel('Distancia (unidades astronómicas)', fontsize=12)
    ax.set_ylabel('Distancia (unidades astronómicas)', fontsize=12)

    # Añadir un fondo
    ax.set_facecolor('black')

    # Sol en el centro
    sun = plt.scatter(0, 0, color='gold', s=300, edgecolor='orange', label='Sol')  
    # Planeta 1
    planet1, = plt.plot([], [], 'o', color='blue', markersize=10, label='Planeta 1')  
    # Planeta 2
    planet2, = plt.plot([], [], 'o', color='red', markersize=10, label='Planeta 2')  

    # Función de inicialización
    def init():
        planet1.set_data([], [])
        planet2.set_data([], [])
        return planet1, planet2,

    # Función de actualización para la animación
    def update(frame):
        planet1.set_data(x1[frame], y1[frame])
        planet2.set_data(x2[frame], y2[frame])
        return planet1, planet2,

    # Crear la animación
    ani = FuncAnimation(fig, update, frames=len(x1), init_func=init, blit=True, interval=100)

    # Mostrar leyenda
    ax.legend(frameon=True, loc='upper right', fontsize=12, shadow=True)
    plt.show()

#graficar funciones trigonométricas
def graficar_funciones_trigonometricas(funcion, rango):
    x = np.linspace(rango[0], rango[1], 1000)  # Genera 1000 puntos en el rango especificado

    if funcion == 'seno':
        y = np.sin(x)
        plt.title('Gráfico de la función seno')
    elif funcion == 'coseno':
        y = np.cos(x)
        plt.title('Gráfico de la función coseno')
    elif funcion == 'tangente':
        y = np.tan(x)
        plt.title('Gráfico de la función tangente')
        plt.ylim(-10, 10)  # Limitar el rango de y para la tangente
        plt.plot(x, y)
        plt.xlabel('x')
        plt.ylabel(f'f(x) = {funcion}(x)')
        plt.grid()
        plt.axhline(0, color='black', lw=0.5, ls='--')
        plt.axvline(0, color='black', lw=0.5, ls='--')
        plt.show()
    else:
        hablar("Función no reconocida. Usa 'seno', 'coseno' o 'tangente'.")
        return



#movimientos de física
def simular_proyectil(velocidad, angulo, tiempo):
    g = 9.81  # Aceleración debido a la gravedad (m/s^2)

    # Convertir el ángulo a radianes
    angulo_rad = np.radians(angulo)

    # Calcular las componentes de la velocidad
    v_x = velocidad * np.cos(angulo_rad)
    v_y = velocidad * np.sin(angulo_rad)

    # Tiempo de vuelo
    t_vuelo = (2 * v_y) / g

    # Crear un array de tiempo
    t = np.linspace(0, min(t_vuelo, tiempo), num=100)

    # Ecuaciones de movimiento
    x = v_x * t
    y = (v_y * t) - (0.5 * g * t**2)

    # Crear la figura para la animación
    fig, ax = plt.subplots(figsize=(10, 5))
    ax.set_xlim(0, max(x) + 1)
    ax.set_ylim(0, max(y) + 1)
    ax.set_title('Simulación del Lanzamiento del Proyectil')
    ax.set_xlabel('Distancia (m)')
    ax.set_ylabel('Altura (m)')
    ax.grid()

    # Inicializar la línea que representará el proyectil
    line, = ax.plot([], [], 'ro', markersize=10)  # Proyectil en rojo

    # Función de inicialización
    def init():
        line.set_data([], [])
        return line,

    # Función de actualización para la animación
    def update(frame):
        line.set_data(x[frame], y[frame])
        return line,

    # Crear la animación
    ani = FuncAnimation(fig, update, frames=len(x), init_func=init, blit=True, interval=100)

    plt.show()  # Mostrar la animación

    # Graficar la trayectoria final
    plt.figure(figsize=(10, 5))
    plt.plot(x, y)
    plt.title('Trayectoria del Proyectil')
    plt.xlabel('Distancia (m)')
    plt.ylabel('Altura (m)')
    plt.grid()
    plt.axhline(0, color='black', lw=0.5, ls='--')
    plt.axvline(0, color='black', lw=0.5, ls='--')
    plt.xlim(0, max(x) + 1)
    plt.ylim(0, max(y) + 1)
    plt.show()

def ejecutar_simulacion(velocidad, angulo, tiempo):
    try:
        velocidad = float(velocidad)
        angulo = float(angulo)
        tiempo = float(tiempo)

        simular_proyectil(velocidad, angulo, tiempo)
    except ValueError:
        messagebox.showerror("Error", "Por favor, ingresa valores numéricos válidos.")

def interfaz_usuario():
    # Crear la ventana principal
    ventana = tk.Tk()
    ventana.title("Simulación de Lanzamiento de Proyectil")

    # Crear etiquetas y entradas
    label_velocidad = tk.Label(ventana, text="Velocidad (m/s):")
    label_velocidad.pack()
    entry_velocidad = tk.Entry(ventana)
    entry_velocidad.pack()

    label_angulo = tk.Label(ventana, text="Ángulo (grados):")
    label_angulo.pack()
    entry_angulo = tk.Entry(ventana)
    entry_angulo.pack()

    label_tiempo = tk.Label(ventana, text="Tiempo de simulación (s):")
    label_tiempo.pack()
    entry_tiempo = tk.Entry(ventana)
    entry_tiempo.pack()

    # Botón para ejecutar la simulación
    boton_simular = tk.Button(ventana, text="Simular", command=lambda: ejecutar_simulacion(entry_velocidad.get(), entry_angulo.get(), entry_tiempo.get()))
    boton_simular.pack()

    # Iniciar la interfaz
    ventana.mainloop



def convertir_a_numero(texto):
    numeros = {
        'cero': 0,
        'uno': 1,
        'dos': 2,
        'tres': 3,
        'cuatro': 4,
        'cinco': 5,
        'seis': 6,
        'siete': 7,
        'ocho': 8,
        'nueve': 9,
        'diez': 10
    }
    return numeros.get(texto, None)

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

def Creador():
    respuesta = ("Quién es mi creador?, pues, es Daniel. Hasta donde tengo memoria, él es mi creador, y según la información que tengo de él es un buen programador, y sencillamente puede ayudarles en lo que necesiten saber acerca de la tecnología.")
    hablar (respuesta)
    
def profe_jesus():
    respuesta_2 = ("¿qué?, ¿De quién hablas?, ¿Jesús garcia?, Ah, Okey, tu profesor de física, claro, cómo no acordarme de él. Señor, quiero decirle, que daniel está agradecido por dejarle participar en este pequeño evento, y quizás en un futuro no muy lejano pueda llegar a ser una buena Inteligencia artificial, solo que necesitaré bastante apoyo. Y no me pareció que haya pre informado a Daniel, oyó?. No mentira, es chiste jeje")
    hablar(respuesta_2)
def profe_jorge():
    respuesta_3 = ("Hola, estimado Rector Jorge Torres, cómo está?, yo estoy bien, gracias a Dios, mi nombe es colmet, como lo he dicho anteriormente." "Por allí me han dicho que usted es el rector de este gran colegio, y claro, cómo no podrían serlo, si son de los mejores colegios a nivel nacional, o bueno, es lo que mis fuentes y bases de datos me proporcionaron. Pero, así mismo quiero agredecerle en nombre de todos los estudiantes colmetristas, por brindarnos una educación de calidad y beneficios. Y nada, sin más qué decir, gracias")
    hablar(respuesta_3)
#traducir a inglés o hablar
def traducir_a_ingles(texto):
    try:
        traduccion = translator.translate(texto, dest='en')
        return traduccion.text
    except Exception as e:
        hablar("Lo siento, no pude traducir el texto.")
        return None



def despedirse():
    hablar(f"Hasta luego Señor, tenga un buen día, un gusto conocer a todas estas personas. Y ustedes muchachos cuídense.")

def escuchar_comando():

    with sr.Microphone() as source:
        print("Te escucho...")
        recognizer.adjust_for_ambient_noise(source,duration=1)


        try:

            audio = recognizer.listen(source,timeout=6,phrase_time_limit=5)
            
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
    elif 'qué es' in comando or 'que es' in comando:
        concepto = comando.replace('qué es ', '').replace('definir ', '').strip()
        definir_concepto(concepto)



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

    elif 'diseñar órbita' in comando:
        hablar("Diseñando órbita de los planetas")
        #Parámetros de la elipse
        a = 5 #semieje mayor del planeta 1
        b = 4 #semieje menor del planeta 1
        c = 3 #semieje mayor del planeta 2
        d = 2 #Semieje menor del planeta 2
        animar_orbita(a, b, c, d)


    elif 'simular lanzamiento de proyectil' in comando:
        hablar("Iniciando la interfaz de simulación de lanzamiento de proyectil.")
        interfaz_usuario()  # Llama a la interfaz de usuario
        hablar("He simulado el lanzamiento de un proyectil")


    # EXPERIMENTO FISICA
    elif 'iniciar experimento' in comando or 'simulación de parábola' in comando:
        hablar("Iniciando simulación de parábola en el aire")
        Experimento()
        hablar("""Simulación finalizada,
        esta simulacion, 
        desarrollada por Cervantes para contribuir en mis funcionalidades,
        representa el movimiento parablico, 
        una clase de fisica que, 
        en nuestro colegio fue dada por el profe Jesus Garcia.
        El movimiento parabólico es un tipo de movimiento que sigue una trayectoria en forma de parábola. 
        Ocurre cuando un objeto es lanzado hacia arriba y al frente, 
        bajo la influencia de la gravedad,
        y su desplazamiento se descompone en dos componentes
        ¿En qué más puedo ayudarte?""")



    elif  'sistema binario' in comando or 'sistema binario' in comando:
        hablar("¿Cuál es la duración de la simulación en segundos? ")
        duracion_input = escuchar_comando()
        duracion = convertir_a_numero(duracion_input)
        if duracion is None:
            hablar("Lo siento, no entendí la duración. Por favor, usa números del cero al diez.")
            continue
        hablar("¿Cuál es el intervalo en segundo")
        intervalo_input = escuchar_comando()
        intervalo = convertir_a_numero(intervalo_input)
        if intervalo is None:
            hablar("Lo siento, no entendí el intervalo")
            continue
        graficar_sistema_binario(duracion, intervalo)
        hablar("He graficado el sistema binario. en qué más puedo ayudar?")



    elif 'función trigonométrica' in comando:
        hablar("¿Qué función trigonométrica deseas graficar? Puedes decir 'seno', 'coseno' o 'tangente'.")
        funcion_a_graficar = escuchar_comando()  # Escuchar la respuesta del usuario
        if 'seno' in comando:
            rango = (-2 * np.pi, 2 * np.pi)  # Rango para la función seno
            graficar_funciones_trigonometricas('seno', rango)
            hablar('graficando el seno')
        elif 'coseno' in comando:
            rango = (-2 * np.pi, 2 * np.pi)  # Rango para la función coseno
            graficar_funciones_trigonometricas('coseno', rango)
            hablar('graficando el coseno')
        elif 'tangente' in comando:
            rango = (-2 * np.pi, 2 * np.pi)  # Rango para la función tangente
            graficar_funciones_trigonometricas('tangente', rango)
            hablar('graficando la tangente')
        else:
            hablar("No entendí qué función deseas graficar.")



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
    


    #traducción, hablar
    elif 'traduce al inglés' in comando or 'speak in english' in comando:
        texto_a_traducir = comando.replace('traduce al inglés', '').strip()
        traduccion = traducir_a_ingles(texto_a_traducir)
        if traduccion:
            hablar(f"La traducción es: {traduccion}")
        elif comando.isascii():
            hablar(f"Has hablado en inglés: {comando}")
        else:
            hablar(f"Has hablado en español")
    


    elif 'cuál es tu creador' in comando:
        Creador()
    
    elif 'dile algo' in comando:
        profe_jesus()
    
    elif 'saluda' in comando or 'saludar' in comando:
        profe_jorge()
    
    
    
    #despedidas
    elif 'gracias, adiós' in comando or 'hasta luego' in comando or 'chau' in comando:
        despedirse()
        break
    else:
        hablar("no entendí tu petición, ¿puedes repetir?, el margen de error que tengo es alto, Daniel solo me creó para cumplir funciones específicas, y los parámetros con los que me han hecho son pocos. En razón de ello, por favor no me pidas cosas que están fuera de mis capacidades ")
# en caso dado no entienda la petición

