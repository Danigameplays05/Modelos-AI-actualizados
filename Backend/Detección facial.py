import cv2
import mediapipe as mp
import time
import numpy as np
from datetime import datetime

# Inicializar MediaPipe
mp_face_mesh = mp.solutions.face_mesh
mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

# Inicializar detectores
face_mesh = mp_face_mesh.FaceMesh(
    max_num_faces=4,
    refine_landmarks=True,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5)

hands = mp_hands.Hands(
    model_complexity=0,
    min_detection_confidence=0.5,
    min_tracking_confidence=0.5,
    max_num_hands=2)

# Inicializar la captura de video
cap = cv2.VideoCapture(0)
cap.set(3, 1280)
cap.set(4, 720)

# Variables para FPS
pTime = 0

def detect_hand_gesture(hand_landmarks):
    """Detecta gestos básicos de la mano"""
    # Obtener puntos clave de los dedos
    thumb_tip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y
    thumb_ip = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_IP].y
    index_tip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y
    index_pip = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_PIP].y
    middle_tip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y
    middle_pip = hand_landmarks.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_PIP].y

    # Detectar gestos básicos
    if thumb_tip < thumb_ip and index_tip < index_pip and middle_tip < middle_pip:
        return "✌️ eaaa"
    elif thumb_tip > thumb_ip and index_tip > index_pip and middle_tip > middle_pip:
        return "👊 Puño"
    elif thumb_tip < thumb_ip and index_tip < index_pip:
        return "🤘 Rock"
    else:
        return "✋ holaaa"

def add_info_panel(img, fps, face_count, hand_count):
    """Añade panel de información"""
    h, w = img.shape[:2]
    overlay = img.copy()
    cv2.rectangle(overlay, (10, 10), (250, 140), (0, 0, 0), -1)
    alpha = 0.4
    img = cv2.addWeighted(overlay, alpha, img, 1 - alpha, 0)

    cv2.putText(img, f'FPS: {int(fps)}', (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(img, f'Rostros: {face_count}', (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    cv2.putText(img, f'Manos: {hand_count}', (20, 120),
                cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)
    
    return img

while cap.isOpened():
    success, image = cap.read()
    if not success:
        print("Ignoring empty camera frame.")
        continue

    # Convertir imagen a RGB
    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    image.flags.writeable = False
    
    # Procesar imagen
    face_results = face_mesh.process(image)
    hand_results = hands.process(image)
    
    image.flags.writeable = True
    image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

    face_count = 0
    hand_count = 0

    # Dibujar rostros (solo mesh, sin partes específicas)
    if face_results.multi_face_landmarks:
        for face_landmarks in face_results.multi_face_landmarks:
            face_count += 1
            mp_drawing.draw_landmarks(
                image=image,
                landmark_list=face_landmarks,
                connections=mp_face_mesh.FACEMESH_TESSELATION,
                landmark_drawing_spec=None,
                connection_drawing_spec=mp_drawing_styles.get_default_face_mesh_tesselation_style())

    # Dibujar manos
    if hand_results.multi_hand_landmarks:
        for idx, hand_landmarks in enumerate(hand_results.multi_hand_landmarks):
            hand_count += 1
            
            # Determinar si es mano izquierda o derecha
            handedness = hand_results.multi_handedness[idx].classification[0].label
            color = (255, 0, 0) if handedness == "Left" else (0, 0, 255)  # Azul para izquierda, Rojo para derecha
            
            # Dibujar puntos y conexiones de la mano
            mp_drawing.draw_landmarks(
                image,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
                mp_drawing_styles.get_default_hand_landmarks_style(),
                mp_drawing.DrawingSpec(color=color, thickness=2))

            # Detectar y mostrar gesto
            gesture = detect_hand_gesture(hand_landmarks)
            wrist = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST]
            pos = (int(wrist.x * image.shape[1]), int(wrist.y * image.shape[0]))
            cv2.putText(image, gesture, pos, 
                       cv2.FONT_HERSHEY_SIMPLEX, 1, color, 2)

    # Calcular FPS
    cTime = time.time()
    fps = 1 / (cTime - pTime)
    pTime = cTime

    # Añadir panel de información
    image = add_info_panel(image, fps, face_count, hand_count)

    # Mostrar imagen
    cv2.imshow('Face Mesh and Hands', image)
    if cv2.waitKey(5) & 0xFF == 27:
        break

cap.release()
cv2.destroyAllWindows()
