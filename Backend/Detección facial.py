import cv2

# Cargar el clasificador en cascada para detección de rostros
cascada_rostros = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

# Iniciar la captura de video desde la cámara
captura = cv2.VideoCapture(0)

while True:
    # Leer un frame de la cámara
    ret, frame = captura.read()
    if not ret:
        break

    # Convertir el frame a escala de grises
    gris = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Detectar rostros en el frame
    rostros = cascada_rostros.detectMultiScale(gris, scaleFactor=1.1, minNeighbors=5)

    # Dibujar un rectángulo alrededor de cada rostro detectado
    for (x, y, w, h) in rostros:
        cv2.rectangle(frame, (x, y), (x + w, y + h), (255, 0, 0), 2)

    # Mostrar el frame con los rostros detectados
    cv2.imshow('Detector de Rostros', frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura y cerrar las ventanas
captura.release()
cv2.destroyAllWindows()