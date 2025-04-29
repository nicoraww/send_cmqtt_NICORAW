import streamlit as st
import paho.mqtt.client as paho
import time
import json
import platform

# Mostrar la versión de Python
st.write("Versión de Python:", platform.python_version())

# Inicializar estado de tema
def init_theme()
# Historial de valores enviados
if 'history' not in st.session_state:
    st.session_state.history = []:
    if 'theme' not in st.session_state:
        st.session_state.theme = 'gray'
init_theme()

# Funciones MQTT callbacks
def on_publish(client, userdata, result):
    st.write("Dato publicado.")

def on_message(client, userdata, message):
    msg = message.payload.decode('utf-8')
    st.write(f"Mensaje recibido: {msg}")

# Configurar CSS según tema
def set_theme_css():
    if st.session_state.theme == 'light':
        bg = '#FFFFFF'
        fg = '#000000'
    elif st.session_state.theme == 'dark':
        bg = '#000000'
        fg = '#FFFFFF'
    else:  # gray
        bg = '#DDDDDD'
        fg = '#000000'
    st.markdown(f"""
    <style>
        html, body, [data-testid="stAppViewContainer"], [data-testid="stSidebar"] {{
            background-color: {bg} !important;
            color: {fg} !important;
        }}
        .stButton > button {{
            background-color: {fg} !important;
            color: {bg} !important;
            border: 1px solid {fg} !important;
        }}
        .stSlider > div {{ color: {fg} !important; }}
        .stTextInput > div > input, .stTextArea > div > textarea, .stNumberInput > div > input {{
            background-color: {bg} !important;
            color: {fg} !important;
            border: 1px solid {fg} !important;
        }}
    </style>
    """, unsafe_allow_html=True)

# Aplicar estilo inicial
set_theme_css()

# Título
st.title("MQTT Control")

# Función para publicar por MQTT
def mqtt_publish(topic, payload):
    client = paho.Client()
    client.on_publish = on_publish
    client.connect("157.230.214.127", 1883)
    client.publish(topic, json.dumps(payload))

# Botones ON/OFF en columnas
t1, t2 = st.columns(2)
with t1:
    if st.button('ON'):
        st.session_state.theme = 'light'
        set_theme_css()
        mqtt_publish('LuzNicoRaw', {"Act1": "ON"})
with t2:
    if st.button('OFF'):
        st.session_state.theme = 'dark'
        set_theme_css()
        mqtt_publish('LuzNicoRaw', {"Act1": "OFF"})

# Slider para valor analógico
value = st.slider('Selecciona valor analógico', 0.0, 100.0, 50.0)
st.write('Valor:', value)

# Botón para enviar valor analógico
if st.button('Enviar valor analógico'):
    mqtt_publish('MotorNicoRaw', {"Analog": float(value)})
    st.write('Valor enviado.')
    # Guardar en historial
    timestamp = time.strftime("%Y-%m-%d %H:%M:%S")
    st.session_state.history.append({"timestamp": timestamp, "value": value})

# Mostrar historial de valores enviados
if st.session_state.history:
    st.subheader('Historial de valores analógicos enviados')
    st.table(st.session_state.history)
