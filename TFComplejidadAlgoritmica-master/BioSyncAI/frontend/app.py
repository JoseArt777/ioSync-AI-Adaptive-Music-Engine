import streamlit as st
import pandas as pd
import requests
import time
import plotly.graph_objs as go
from collections import deque
import os
import sys

# Agregar directorio padre al path para permitir importación directa de logic para el modo "Standalone"
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from backend.logic import BioSyncLogic
from data.mock_data_generator import generate_mock_spotify_data

# Page Config
st.set_page_config(
    page_title="BioSync AI Dashboard",
    page_icon="💓",
    layout="wide"
)

# --- Inyección CSS para UI Dinámica (Solo Visualizador) ---
def inject_visualizer_css(bpm):
    # Calcular velocidad de animación basada en BPM
    anim_duration = f"{60/max(bpm, 1):.2f}s"
    accent_color = "#ff4b4b" # Streamlit's default red accent

    css = f"""
    <style>
        /* Audio Visualizer Bars */
        .visualizer-container {{
            display: flex;
            align-items: flex-end;
            height: 60px;
            gap: 5px;
            margin-top: 20px;
            margin-bottom: 20px;
        }}
        
        .bar {{
            width: 10px;
            background-color: {accent_color};
            animation: bounce {anim_duration} infinite ease-in-out alternate;
            border-radius: 5px 5px 0 0;
        }}
        
        .bar:nth-child(1) {{ height: 40%; animation-delay: 0.1s; }}
        .bar:nth-child(2) {{ height: 70%; animation-delay: 0.3s; }}
        .bar:nth-child(3) {{ height: 100%; animation-delay: 0.0s; }}
        .bar:nth-child(4) {{ height: 60%; animation-delay: 0.4s; }}
        .bar:nth-child(5) {{ height: 80%; animation-delay: 0.2s; }}
        
        @keyframes bounce {{
            0% {{ height: 20%; opacity: 0.5; }}
            100% {{ height: 100%; opacity: 1; }}
        }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

# --- Title and Pitch ---
st.title("💓 BioSync AI")
st.markdown("**Sistema de Recomendación Musical Adaptativo basado en Biofeedback**")
st.markdown("> *\"El entrenador personal invisible que ajusta la música a tu corazón.\"*")

# --- Sidebar: Controles y Configuración ---
st.sidebar.header("Simulación de Sensor")
# Usar session state para ritmo cardíaco para permitir auto-actualizaciones
if 'simulated_hr' not in st.session_state:
    st.session_state.simulated_hr = 90

# Si auto-simulate está OFF, tomamos el valor del slider. 
# Si está ON, ignoramos el input del slider (o lo usamos como base) y actualizamos programáticamente.
auto_simulate = st.sidebar.checkbox("Simular Variación Automática", value=False)

if not auto_simulate:
    heart_rate_input = st.sidebar.slider("Frecuencia Cardíaca (BPM)", 60, 200, st.session_state.simulated_hr)
    st.session_state.simulated_hr = heart_rate_input
else:
    st.sidebar.info(f"Simulando... BPM Actual: {st.session_state.simulated_hr}")
    # ¿Mostrar slider deshabilitado o solo info? Solo mostramos el valor.

st.sidebar.markdown("---")
st.sidebar.subheader("Debug Info")
api_mode = st.sidebar.radio("Modo de Operación", ["Standalone (Direct Python)", "API (FastAPI)"])

# --- Gestión de Estado ---
if 'history_hr' not in st.session_state:
    st.session_state.history_hr = deque(maxlen=50)
if 'history_tempo' not in st.session_state:
    st.session_state.history_tempo = deque(maxlen=50)
if 'current_song' not in st.session_state:
    st.session_state.current_song = None
if 'last_zone' not in st.session_state:
    st.session_state.last_zone = "Unknown"
if 'next_song_switch_time' not in st.session_state:
    st.session_state.next_song_switch_time = 0

# --- Inicialización de Lógica (Modo Standalone) ---
@st.cache_resource
def get_logic_engine():
    # Resolver rutas absolutas basadas en la ubicación de este archivo (frontend/app.py)
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__))) # BioSyncAI/
    real_data_path = os.path.join(base_dir, "data", "dataset.csv")
    mock_data_path = os.path.join(base_dir, "data", "spotify_mock.csv")
    
    if os.path.exists(real_data_path):
        return BioSyncLogic(music_db_path=real_data_path)
    
    if not os.path.exists(mock_data_path):
        df = generate_mock_spotify_data()
        os.makedirs(os.path.join(base_dir, "data"), exist_ok=True)
        df.to_csv(mock_data_path, index=False)
    return BioSyncLogic(music_db_path=mock_data_path)

logic = get_logic_engine()

# --- Simulación de Bucle Principal ---
heart_rate = st.session_state.simulated_hr

# Lógica de Auto-Simulación
if auto_simulate:
    import numpy as np
    # Caminata aleatoria: pequeño cambio respecto al anterior
    change = np.random.randint(-3, 4) 
    heart_rate += change
    # Limitar valores
    heart_rate = max(60, min(200, heart_rate))
    st.session_state.simulated_hr = heart_rate

# Input Chatbot NLP
st.sidebar.markdown("---")
st.sidebar.subheader("💬 AI Chatbot")
user_message = st.sidebar.text_input("¿Cómo te sientes?", placeholder="Ej: Estoy agotado / Tengo energía")

# Obtener Lógica de Recomendación (con Persistencia)
current_time = time.time()
current_song_id = st.session_state.current_song['track_id'] if st.session_state.current_song else None

# Decidir si necesitamos una nueva canción
should_fetch_new_song = False
if st.session_state.current_song is None:
    should_fetch_new_song = True
elif current_time >= st.session_state.next_song_switch_time:
    should_fetch_new_song = True

song = st.session_state.current_song
zone = st.session_state.last_zone
fatigue_risk = False
if 'last_sentiment_label' not in st.session_state:
    st.session_state.last_sentiment_label = "Neutral"
if 'last_bot_response' not in st.session_state:
    st.session_state.last_bot_response = "Esperando tu estado..."

if should_fetch_new_song:
    # Preparar historial para predicción de fatiga
    hr_history_list = list(st.session_state.history_hr)
    
    if api_mode == "Standalone (Direct Python)":
        # Análisis de NLP (Centralizado)
        sentiment_adjustment, sentiment_label, bot_response = logic.analyze_sentiment(user_message)
        
        if user_message:
            st.session_state.last_sentiment_label = sentiment_label
            st.session_state.last_bot_response = bot_response
            
        new_song, new_zone = logic.recommend_song(heart_rate, current_song_id, sentiment_adjustment)
        fatigue_risk = logic.predict_fatigue(hr_history_list)
        
    else:
        # Llamada a API
        try:
            payload = {
                "heart_rate": heart_rate, 
                "current_song_id": current_song_id,
                "user_message": user_message,
                "hr_history": hr_history_list
            }
            response = requests.post("http://127.0.0.1:8000/recommend", json=payload)
            if response.status_code == 200:
                data = response.json()
                new_song = data['recommended_song']
                new_zone = data['zone']
                fatigue_risk = data.get('fatigue_risk', False)
                st.session_state.last_sentiment_label = data.get('sentiment_analysis', "Neutral")
                # Respuesta fallback simple para modo API (puede mejorarse en backend luego)
                if "Positivo" in st.session_state.last_sentiment_label:
                    st.session_state.last_bot_response = "¡Modo Bestia activado! Vamos a romperla 🚀"
                elif "Negativo" in st.session_state.last_sentiment_label:
                    st.session_state.last_bot_response = "Entendido. Bajando revoluciones, recupera el aliento. 🧘"
                else:
                    st.session_state.last_bot_response = "Sigo analizando tus biometría..."
            else:
                st.error("Error connecting to API")
                new_song, new_zone = None, "Error"
        except:
            new_song, new_zone = None, "Connection Error"
    
    if new_song:
        song = new_song
        zone = new_zone
        DEMO_SONG_DURATION = 10 
        st.session_state.next_song_switch_time = current_time + DEMO_SONG_DURATION
        
        st.session_state.current_song = song
        st.session_state.last_zone = zone

# Siempre actualizar historial para gráfica
st.session_state.history_hr.append(heart_rate)
if song:
    st.session_state.history_tempo.append(song['tempo'])
else:
    st.session_state.history_tempo.append(0)

# --- Layout del Dashboard ---

col1, col2 = st.columns([1, 2])

with col1:
    st.subheader("Estado Actual")
    st.metric(label="❤️ Ritmo Cardíaco", value=f"{heart_rate} BPM", delta=f"{heart_rate - 90} vs Reposo")
    
    # Alerta de Fatiga
    if fatigue_risk:
        st.error("⚠️ ALERTA DE FATIGA DETECTADA")
        st.caption("La Red Neuronal predice agotamiento inminente. Bajando intensidad...")
    
    if user_message:
        with st.chat_message("user"):
            st.write(user_message)
            
        with st.chat_message("assistant"):
            st.markdown(f"**🧠 Análisis:** {st.session_state.last_sentiment_label}")
            st.write(f"{st.session_state.last_bot_response}")

    zone_color = "grey"
    if zone == "Rest/Warmup": zone_color = "blue"
    elif zone == "Fat Burn": zone_color = "green"
    elif zone == "Cardio": zone_color = "orange"
    elif zone == "Peak Performance": zone_color = "red"
    
    st.markdown(f"### Zona: :{zone_color}[{zone}]")
    
    if st.session_state.current_song:
        st.markdown("---")
        
        # Inyectar CSS para visualizador (mantenemos esto para los keyframes de animación)
        inject_visualizer_css(heart_rate)
        
        # HTML de Tarjeta de Reproductor Unificada
        song = st.session_state.current_song
        player_html = f"""
<div style="background-color: #f0f2f6; padding: 20px; border-radius: 10px; border-left: 5px solid #ff4b4b; box-shadow: 0 4px 6px rgba(0,0,0,0.1);">
<h3 style="margin-top: 0; color: #333;">🎵 Reproduciendo Ahora</h3>
<div style="font-size: 1.2em; font-weight: bold; color: #000;">{song['track_name']}</div>
<div style="color: #666; margin-bottom: 10px;">👤 {song['artist_name']}</div>
<div style="display: flex; justify-content: space-between; font-size: 0.9em; color: #444;">
<span>🎹 Tempo: <b>{song['tempo']} BPM</b></span>
<span>⚡ Energía: <b>{song['energy']}</b></span>
</div>
<!-- Visualizador Dentro de la Tarjeta -->
<div class="visualizer-container" style="margin-top: 15px; margin-bottom: 5px; height: 40px;">
<div class="bar"></div>
<div class="bar"></div>
<div class="bar"></div>
<div class="bar"></div>
<div class="bar"></div>
</div>
</div>
"""
        st.markdown(player_html, unsafe_allow_html=True)

        # Barra de Progreso para Canción (¿mantener fuera o integrar? Fuera está bien por ahora)
        time_left = max(0, int(st.session_state.next_song_switch_time - current_time))
        st.caption(f"Siguiente cambio en: {time_left}s")
        st.progress(max(0.0, min(1.0, 1 - (time_left / 10.0)))) 
    else:
        st.warning("Esperando datos...")

with col2:
    st.subheader("Sincronización en Tiempo Real")
    
    # Graficado
    if len(st.session_state.history_hr) > 0:
        fig = go.Figure()
        
        fig.add_trace(go.Scatter(
            y=list(st.session_state.history_hr),
            mode='lines+markers',
            name='Ritmo Cardíaco (User)',
            line=dict(color='firebrick', width=3)
        ))
        
        fig.add_trace(go.Scatter(
            y=list(st.session_state.history_tempo),
            mode='lines',
            name='Música BPM (System)',
            line=dict(color='royalblue', width=3, dash='dot')
        ))
        
        fig.update_layout(
            title="Bio-Music Synchronization",
            xaxis_title="Tiempo (segundos simulados)",
            yaxis_title="BPM",
            template="plotly_white",
            height=400,
            yaxis=dict(range=[50, 210]) # Fijar eje y para evitar saltos
        )
        
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("Inicia la simulación para ver la gráfica.")

# --- Pie de página / Explicación ---
st.markdown("---")
st.markdown("### 🧠 Cómo funciona BioSync AI")
st.markdown("""
1.  **Input**: Simula la entrada de un sensor Galaxy Watch (Heart Rate).
2.  **Inferencia**: El sistema clasifica el esfuerzo en zonas (Calentamiento, Cardio, Pico).
3.  **Matching**: Busca en la base de datos vectorial (simulada) una canción con el BPM y Energía óptimos.
4.  **Feedback**: Visualiza cómo la música 'empuja' o 'sigue' al usuario.
""")

# Auto-Rerun al final
if auto_simulate:
    time.sleep(1) # Esperar 1 segundo antes de la siguiente actualización
    st.rerun()
