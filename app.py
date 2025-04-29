import os
import random
import string
import platform
import streamlit as st
import numpy as np
from PIL import Image as PILImage
from keras.models import load_model

# Mostrar la versión de Python
st.write("Versión de Python:", platform.python_version())

# Cargar modelo
dir_path = os.path.dirname(__file__)
model_path = os.path.join(dir_path, 'keras_model.h5')
model = load_model(model_path)

# Título
st.title("Reconocimiento de Gestos de Mano")

with st.sidebar:
    st.subheader("📷 Captura")
    st.write("Usa la cámara para capturar el gesto de tu mano y el modelo predecirá si está abierta o cerrada.")

# Input de cámara
img_buffer = st.camera_input("Toma una foto:")

if img_buffer is not None:
    # Preprocesamiento de la imagen
    img = PILImage.open(img_buffer).convert('RGB')
    img = img.resize((224, 224))
    img_array = np.array(img, dtype=np.float32)
    normalized = (img_array / 127.5) - 1
    data = normalized.reshape((1, 224, 224, 3))

    # Predicción
    prediction = model.predict(data)[0]
    open_prob, closed_prob = prediction[0], prediction[1]

    # Mostrar probabilidades
    st.write(f"Probabilidad Mano Abierta: {open_prob:.2f}")
    st.write(f"Probabilidad Mano Cerrada: {closed_prob:.2f}")

    # Generar salida aleatoria
    if open_prob > closed_prob:
        # Mano abierta: letra aleatoria
        letter = random.choice(string.ascii_uppercase)
        st.header(f"✋ Mano Abierta → Letra: {letter}")
    else:
        # Mano cerrada: número aleatorio
        number = random.randint(1, 100)
        st.header(f"✊ Mano Cerrada → Número: {number}")

    # Limpieza de archivos temporales (opcional)
    # Aquí podrías eliminar imágenes temporales si las guardaste en disco
