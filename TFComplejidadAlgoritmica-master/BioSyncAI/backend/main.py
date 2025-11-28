from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import os
import sys

# Agregar directorio padre al path para importar logic si es necesario
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from backend.logic import BioSyncLogic
from data.mock_data_generator import generate_mock_spotify_data

app = FastAPI(title="BioSync AI API", description="API for Adaptive Music Recommendation")

# Inicializar Lógica
# Verificar dataset real primero, luego mock
real_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "dataset.csv")
mock_data_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "spotify_mock.csv")

if os.path.exists(real_data_path):
    print(f"Loading real dataset from {real_data_path}")
    logic_engine = BioSyncLogic(music_db_path=real_data_path)
else:
    print("Real dataset not found. Generating mock data...")
    if not os.path.exists(mock_data_path):
        df = generate_mock_spotify_data()
        df.to_csv(mock_data_path, index=False)
    logic_engine = BioSyncLogic(music_db_path=mock_data_path)

from typing import Optional

from typing import Optional, List

class BioFeedbackInput(BaseModel):
    heart_rate: int
    current_song_id: Optional[str] = None
    user_message: Optional[str] = None
    hr_history: Optional[List[int]] = []

@app.get("/")
def read_root():
    return {"message": "BioSync AI API is running"}

@app.post("/recommend")
def recommend_music(feedback: BioFeedbackInput):
    # Análisis de NLP (Centralizado)
    sentiment_adjustment, sentiment_label, bot_response = logic_engine.analyze_sentiment(feedback.user_message)

    # Recomendación con IA (RF + K-Means)
    song, zone = logic_engine.recommend_song(feedback.heart_rate, feedback.current_song_id, sentiment_adjustment)
    
    # Predicción de Fatiga (MLP)
    fatigue_risk = logic_engine.predict_fatigue(feedback.hr_history)
    
    if not song:
        raise HTTPException(status_code=404, detail="No suitable song found")
    
    return {
        "zone": zone,
        "recommended_song": song,
        "fatigue_risk": fatigue_risk,
        "sentiment_analysis": sentiment_label
    }
