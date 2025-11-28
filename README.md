# BioSync AI: Motor de Música Adaptativa con Biofeedback

> **Proyecto desarrollado en el contexto del Samsung Innovation Campus (Python & AI Program)**

## 📋 Descripción del Proyecto

**BioSync AI** es un sistema inteligente de recomendación musical que sincroniza la música con el estado fisiológico y emocional del usuario en tiempo real.

El problema que resuelve es la desconexión entre la música que escuchamos y nuestro estado físico durante actividades como el ejercicio o la relajación. A diferencia de las listas de reproducción estáticas, BioSync AI actúa como un "entrenador invisible", ajustando dinámicamente el tempo y la energía de la música para optimizar el rendimiento cardiovascular o facilitar la recuperación, basándose en datos biométricos simulados (ritmo cardíaco) y análisis de sentimiento.

## ✨ Características Principales

*   **Sincronización Biométrica en Tiempo Real:** Ajusta la música según la frecuencia cardíaca del usuario.
*   **Análisis de Sentimiento (NLP):** Chatbot integrado que interpreta el estado emocional del usuario para refinar las recomendaciones.
*   **Detección de Fatiga con Deep Learning:** Monitorea el historial de ritmo cardíaco para predecir y alertar sobre riesgos de agotamiento.
*   **Clasificación de Zonas de Entrenamiento:** Determina automáticamente si el usuario está en zona de Calentamiento, Quema de Grasa, Cardio o Rendimiento Máximo.
*   **Dashboard Interactivo:** Visualización en tiempo real de métricas, zonas y control de reproducción.

## 🛠️ Tecnologías Utilizadas

Este proyecto implementa una arquitectura moderna de Inteligencia Artificial y Desarrollo Web:

### Backend & API
*   **Python 3.10+**: Lenguaje núcleo del proyecto.
*   **FastAPI**: Framework de alto rendimiento para la creación de la API RESTful.
*   **Uvicorn**: Servidor ASGI para producción.

### Inteligencia Artificial & Data Science
*   **Scikit-learn**:
    *   *K-Means Clustering*: Para agrupación no supervisada de canciones por `tempo` y `energy`.
    *   *Random Forest Classifier*: Para clasificación supervisada de zonas de entrenamiento.
    *   *MLPClassifier (Red Neuronal)*: Para la predicción de patrones de fatiga secuenciales.
*   **Pandas & NumPy**: Manipulación y análisis de estructuras de datos.
*   **NLP (Procesamiento de Lenguaje Natural)**: Lógica personalizada para análisis de sentimiento con manejo de negaciones e intensificadores.

### Frontend
*   **Streamlit**: Framework para la creación rápida de dashboards de datos interactivos.
*   **Plotly**: Librería de graficado dinámico para visualizar la sincronización música-corazón.

## ⚙️ Requisitos Previos

*   Python 3.10 o superior instalado.
*   Git instalado.

## 🚀 Instrucciones de Instalación y Ejecución

Sigue estos pasos para ejecutar el proyecto en tu entorno local:

1.  **Clonar el repositorio:**
    ```bash
    git clone https://github.com/tu-usuario/ioSync-AI-Adaptive-Music-Engine.git
    cd ioSync-AI-Adaptive-Music-Engine
    ```

2.  **Instalar dependencias:**
    Se recomienda usar un entorno virtual (`venv` o `conda`).
    ```bash
    pip install -r BioSyncAI/requirements.txt
    ```

3.  **Ejecutar el Backend (API):**
    En una terminal, inicia el servidor:
    ```bash
    uvicorn BioSyncAI.backend.main:app --reload
    ```
    *El servidor iniciará en `http://127.0.0.1:8000`*

4.  **Ejecutar el Frontend (Dashboard):**
    En una **nueva** terminal, inicia la interfaz:
    ```bash
    streamlit run BioSyncAI/frontend/app.py
    ```
    *La aplicación se abrirá automáticamente en tu navegador en `http://localhost:8501`*

## 📂 Estructura del Proyecto

```text
BioSyncAI/
├── backend/
│   ├── main.py          # Punto de entrada de la API (FastAPI)
│   └── logic.py         # Núcleo de IA (Modelos ML, Lógica de Negocio)
├── frontend/
│   └── app.py           # Interfaz de Usuario (Streamlit)
├── data/
│   ├── dataset.csv      # Base de datos musical (Spotify Tracks)
│   └── mock_data...     # Generadores de datos sintéticos para pruebas
└── requirements.txt     # Lista de dependencias del proyecto
```

## 🔌 Endpoints de la API

La API expone los siguientes endpoints principales:

*   **`POST /recommend`**: Recibe datos biométricos y retorna la canción recomendada.
    *   *Body:* `{ "heart_rate": 120, "current_song_id": "...", "user_message": "...", "hr_history": [...] }`
    *   *Response:* `{ "recommended_song": {...}, "zone": "Fat Burn", "fatigue_risk": false }`

## 📸 Ejemplos de Uso

1.  **Inicio:** Al abrir la app, el sistema simula un ritmo cardíaco base (ej. 90 BPM).
2.  **Interacción:** El usuario puede usar el slider para simular un aumento de intensidad (ej. subir a 140 BPM).
3.  **Respuesta:**
    *   El sistema detecta el cambio a zona "Cardio".
    *   El algoritmo selecciona una canción con mayor BPM y Energía.
    *   Si el usuario escribe "Estoy agotado" en el chat, el sistema prioriza canciones de recuperación.

## ✅ Buenas Prácticas Implementadas

*   **Arquitectura Modular:** Separación clara entre lógica de negocio (`logic.py`), API (`backend`) y Presentación (`frontend`).
*   **Manejo de Errores:** Fallbacks robustos (uso de datos mock si no hay dataset real).
*   **Tipado Estático:** Uso de `Pydantic` para validación de datos en la API.
*   **Clean Code:** Estructura legible y documentada.

## 🎓 Aprendizajes Obtenidos

Este proyecto permitió consolidar conocimientos en:
*   Integración de modelos de Machine Learning en aplicaciones web productivas.
*   Diseño de arquitecturas cliente-servidor asíncronas.
*   Manejo de estado y flujos de datos en tiempo real con Streamlit.
*   Implementación de algoritmos de clustering y clasificación aplicados a problemas reales.

## 🔮 Posibles Mejoras Futuras

*   **Integración Hardware:** Conexión vía Bluetooth con bandas cardíacas reales (Polar/Garmin).
*   **API Spotify Real:** Reemplazar el dataset estático por la API de Spotify para reproducción real.
*   **Modelos LSTM:** Implementar redes recurrentes para una predicción de fatiga más precisa a largo plazo.

---
*Autor: Jose Alexander Lopez Lopez*
