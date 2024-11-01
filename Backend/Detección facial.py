import cv2
import face_recognition

# Cargar imágenes de referencia y aprender a reconocerlas
imagen_conocida = face_recognition.load_image_file("ruta/a/tu/imagen_conocida.jpg")
nombre_conocido = "Nombre de la Persona"  # Cambia esto por el nombre correspondiente

# Codificar la imagen conocida
codificacion_conocida = face_recognition.face_encodings(imagen_conocida)[0]

# Iniciar la captura de video desde la cámara
captura = cv2.VideoCapture(0)

while True:
    # Leer un frame de la cámara
    ret, frame = captura.read()
    if not ret:
        break

    # Convertir el frame de BGR a RGB
    rgb_frame = frame[:, :, ::-1]

    # Encontrar todas las caras y sus codificaciones en el frame actual
    caras_en_frame = face_recognition.face_locations(rgb_frame)
    codificaciones_en_frame = face_recognition.face_encodings(rgb_frame, caras_en_frame)

    # Iterar sobre las caras encontradas
    for (top, right, bottom, left), codificacion_en_frame in zip(caras_en_frame, codificaciones_en_frame):
        # Comparar la codificación de la cara actual con la codificación conocida
        coincidencias = face_recognition.compare_faces([codificacion_conocida], codificacion_en_frame)

        nombre = "Desconocido"
        if coincidencias[0]:
            nombre = nombre_conocido

        # Dibujar un rectángulo alrededor de la cara y poner el nombre
        cv2.rectangle(frame, (left, top), (right, bottom), (0, 255, 0), 2)
        cv2.putText(frame, nombre, (left, top - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.75, (0, 255, 0), 2)

    # Mostrar el frame con los rostros detectados y reconocidos
    cv2.imshow('Reconocimiento Facial', frame)

    # Salir del bucle si se presiona la tecla 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Liberar la captura y cerrar las ventanas
captura.release()
cv2.destroyAllWindows()