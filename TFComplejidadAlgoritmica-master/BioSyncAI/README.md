# BioSync AI 💓🎧

**Sistema de Recomendación Musical Adaptativo basado en Biofeedback y Series Temporales.**

Este proyecto demuestra cómo utilizar datos biométricos (ritmo cardíaco) para ajustar dinámicamente la música que escucha un usuario, optimizando su rendimiento deportivo. Ideal para integración con Wearables como Samsung Galaxy Watch.

## 🚀 Inicio Rápido

### 1. Instalación de Dependencias

Asegúrate de tener Python instalado. Navega a la carpeta del proyecto e instala las librerías:

```bash
cd BioSyncAI
pip install -r requirements.txt
```

### 2. Ejecutar la Demo (Dashboard)

La forma más rápida de ver el proyecto en acción es usar el Dashboard de Streamlit. Este dashboard incluye un modo "Standalone" que no requiere ejecutar el backend por separado.

```bash
streamlit run frontend/app.py
```

*   Usa el **slider** en la barra lateral para cambiar tu "Ritmo Cardíaco".
*   Observa cómo cambia la música y la gráfica en tiempo real.

### 3. Arquitectura Completa (Backend + Frontend)

Si deseas probar la arquitectura completa con API REST (FastAPI):

1.  **Terminal 1 (Backend):**
    ```bash
    uvicorn backend.main:app --reload
    ```
    La API estará corriendo en `http://127.0.0.1:8000`.

2.  **Terminal 2 (Frontend):**
    ```bash
    streamlit run frontend/app.py
    ```
    En el dashboard, cambia el "Modo de Operación" a **API (FastAPI)**.

## 📂 Estructura del Proyecto

*   `backend/`: Código del servidor y lógica de negocio.
    *   `main.py`: API FastAPI.
    *   `logic.py`: Algoritmo de clasificación de zonas y recomendación.
*   `frontend/`: Interfaz de usuario.
    *   `app.py`: Dashboard interactivo con Streamlit.
*   `data/`: Manejo de datos.
    *   `mock_data_generator.py`: Genera un dataset simulado de Spotify si no existe.

## 🧠 Lógica del Algoritmo

El sistema mapea el Ritmo Cardíaco (HR) a características musicales:

*   **Calentamiento (90-110 BPM)** -> Música 90-100 BPM, Energía Baja.
*   **Cardio (120-150 BPM)** -> Música 130-160 BPM, Energía Alta.
*   **Pico (>150 BPM)** -> Música >160 BPM, Energía Máxima.

## 🔮 Próximos Pasos (Samsung Integration)

1.  Reemplazar `mock_data_generator.py` con el **Spotify Tracks Dataset** real de Kaggle.
2.  Integrar lectura real de sensores mediante Samsung Health SDK.
