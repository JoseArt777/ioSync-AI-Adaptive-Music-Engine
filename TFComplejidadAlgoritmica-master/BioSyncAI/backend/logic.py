import pandas as pd
import numpy as np
import os
from sklearn.cluster import KMeans
from sklearn.neural_network import MLPClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import StandardScaler

class BioSyncLogic:
    def __init__(self, music_db_path=None):
        # Cargar el conjunto de datos
        if music_db_path and os.path.exists(music_db_path):
            self.music_db = pd.read_csv(music_db_path)
            self.music_db.columns = self.music_db.columns.str.strip()
        else:
            self.music_db = pd.DataFrame()

        # Asegurar que existan las columnas requeridas
        required_columns = ['tempo', 'energy', 'track_id', 'track_name', 'artists']
        if not self.music_db.empty:
            missing = [c for c in required_columns if c not in self.music_db.columns]
            if missing:
                print(f"Warning: Missing columns {missing} in dataset. Using empty DB.")
                self.music_db = pd.DataFrame()
        
        # --- IA 1: Aprendizaje No Supervisado (Clustering) ---
        if not self.music_db.empty:
            self._train_clustering_model()
            
        # --- IA 2: Aprendizaje Supervisado (Clasificación de Zona) ---
        self._train_zone_classifier()
            
        # --- IA 3: Deep Learning (Predicción de Fatiga) ---
        self._train_fatigue_model()

    def _train_clustering_model(self):
        """
        Usa K-Means para agrupar canciones en 4 clusters basados en Tempo y Energía.
        """
        features = self.music_db[['tempo', 'energy']]
        self.scaler = StandardScaler()
        features_scaled = self.scaler.fit_transform(features)
        
        self.kmeans = KMeans(n_clusters=4, random_state=42, n_init=10)
        self.music_db['cluster'] = self.kmeans.fit_predict(features_scaled)
        
        # Mapear clusters a zonas basado en tempo promedio
        cluster_tempos = self.music_db.groupby('cluster')['tempo'].mean().sort_values()
        self.cluster_map = {
            cluster_id: zone_idx 
            for zone_idx, cluster_id in enumerate(cluster_tempos.index)
        }

    def _train_zone_classifier(self):
        """
        Entrena un Clasificador Random Forest para determinar zonas de entrenamiento.
        Reemplaza la lógica simple if/else con un modelo entrenado.
        """
        # Datos de Entrenamiento Simulados (Ritmo Cardíaco, Edad -> Zona)
        # Zonas: 0=Reposo, 1=QuemaGrasa, 2=Cardio, 3=Pico
        X_train = []
        y_train = []
        
        # Generar datos sintéticos
        for _ in range(200):
            # Rest
            X_train.append([np.random.randint(50, 100), 25])
            y_train.append(0)
            # Fat Burn
            X_train.append([np.random.randint(100, 130), 25])
            y_train.append(1)
            # Cardio
            X_train.append([np.random.randint(130, 160), 25])
            y_train.append(2)
            # Peak
            X_train.append([np.random.randint(160, 210), 25])
            y_train.append(3)
            
        self.zone_classifier = RandomForestClassifier(n_estimators=10, random_state=42)
        self.zone_classifier.fit(X_train, y_train)

    def _train_fatigue_model(self):
        """
        Entrena un MLP simple para predecir fatiga basado en historial de RC.
        """
        # Datos de entrenamiento simulados: Secuencia de 5 valores RC -> Fatiga (0/1)
        X_train = np.array([
            [80, 82, 85, 88, 90],   # Normal
            [140, 142, 145, 143, 140], # Estable
            [160, 165, 170, 175, 180], # Aumento rápido (Fatiga)
            [170, 170, 170, 170, 170], # Pico sostenido (Fatiga)
            [90, 90, 90, 90, 90],     # Estable
        ])
        y_train = np.array([0, 0, 1, 1, 0])
        
        self.fatigue_model = MLPClassifier(hidden_layer_sizes=(10, 5), max_iter=1000, random_state=42)
        self.fatigue_model.fit(X_train, y_train)

    def predict_fatigue(self, hr_history):
        if len(hr_history) < 5: return False
        recent_hr = np.array(hr_history[-5:]).reshape(1, -1)
        return bool(self.fatigue_model.predict(recent_hr)[0])

    def determine_zone_ai(self, heart_rate):
        """
        Usa Random Forest para clasificar la zona.
        """
        # Asumir edad 25 para demo
        prediction = self.zone_classifier.predict([[heart_rate, 25]])[0]
        zones = ["Rest/Warmup", "Fat Burn", "Cardio", "Peak Performance"]
        return zones[prediction], prediction

    def get_target_music_features(self, zone):
        # Mantener esto para referencia/fallback
        if zone == "Rest/Warmup": return (60, 100), (0.0, 0.5)
        elif zone == "Fat Burn": return (100, 130), (0.4, 0.7)
        elif zone == "Cardio": return (130, 160), (0.7, 0.9)
        elif zone == "Peak Performance": return (160, 200), (0.8, 1.0)
        return (0, 0), (0, 0)

    def recommend_song(self, heart_rate, current_song_id=None, sentiment_adjustment=0):
        """
        Recomienda una canción usando IA (Random Forest + K-Means).
        """
        # 1. Determinar Zona con Random Forest
        zone_name, zone_idx = self.determine_zone_ai(heart_rate)
        
        # 2. Ajustar cluster objetivo basado en Sentimiento (NLP)
        target_zone_idx = max(0, min(3, zone_idx + int(sentiment_adjustment)))
        
        # 3. Mapear a Cluster K-Means
        target_cluster = None
        for cluster_id, level in self.cluster_map.items():
            if level == target_zone_idx:
                target_cluster = cluster_id
                break
        
        # 4. Filtrar por Cluster
        candidates = self.music_db[self.music_db['cluster'] == target_cluster]
        
        if candidates.empty: candidates = self.music_db
            
        if current_song_id and len(candidates) > 1:
            candidates = candidates[candidates['track_id'] != current_song_id]
            
        if not candidates.empty:
            recommended_song = candidates.sample(1).iloc[0].to_dict()
            if 'artists' in recommended_song and 'artist_name' not in recommended_song:
                recommended_song['artist_name'] = recommended_song['artists']
            return recommended_song, zone_name
        
        return None, zone_name

    def analyze_sentiment(self, message):
        """
        Analiza el sentimiento de un mensaje usando coincidencia avanzada de palabras clave,
        manejo de negaciones e intensificadores.
        Retorna: (puntaje_ajuste, etiqueta, respuesta_bot)
        """
        if not message:
            return 0, "Neutral", "Esperando tu estado..."

        msg = message.lower()
        
        # --- Lógica Avanzada de NLP ---
        # 1. Vocabulario con Pesos
        keywords = {
            # Alta Energía / Positivo (+1 a +2)
            "energía": 2, "fuerte": 2, "tope": 2, "fuego": 2, "máquina": 2, "bestia": 2, "imparable": 2,
            "feliz": 1, "bien": 1, "vamos": 1, "arriba": 1, "excelente": 1, "genial": 1, "activo": 1,
            "motivado": 1, "poder": 1, "rápido": 1, "ganas": 1, "dale": 1, "sigue": 1, "adrenalina": 1,
            "romperla": 2, "duro": 1, "ganar": 1, "fácil": 1, "listo": 1, "go": 1, "volar": 2, "incansable": 2,
            "explotar": 2, "ritmo": 1, "bass": 1, "sube": 1, "max": 1, "locura": 1,
            
            # Baja Energía / Negativo (-1 a -2)
            "cansado": -2, "agotado": -2, "muerto": -2, "asfixiado": -2, "rendirme": -2, "basta": -2, "duele": -2,
            "mal": -1, "triste": -1, "bajar": -1, "descanso": -1, "fatiga": -1, "lento": -1, "dolor": -1,
            "sueño": -1, "pesado": -1, "aburrido": -1, "parar": -1, "no puedo": -2, "aire": -1, "sed": -1,
            "mareado": -2, "calambre": -2, "flojera": -1, "difícil": -1, "imposible": -1, "calma": -1,
            "paz": -1, "suave": -1, "dormir": -1, "estrés": -1, "ansiedad": -1, "rodilla": -2, "espalda": -2, "lesión": -2
        }
        
        negations = ["no", "ni", "nunca", "jamás", "sin", "poco"]
        intensifiers = ["muy", "mucho", "demasiado", "super", "mega", "ultra", "re"]

        words = msg.split()
        score = 0
        
        for i, word in enumerate(words):
            # Limpiar puntuación
            clean_word = word.strip(".,!¡?¿")
            
            if clean_word in keywords:
                val = keywords[clean_word]
                
                # Verificar Negación (mirar atrás 1-2 palabras)
                is_negated = False
                if i > 0 and words[i-1] in negations: is_negated = True
                if i > 1 and words[i-2] in negations: is_negated = True
                
                # Verificar Intensificador (mirar atrás 1 palabra)
                is_intensified = False
                if i > 0 and words[i-1] in intensifiers: is_intensified = True
                
                # Aplicar Lógica
                if is_negated:
                    val = -val # Invertir significado ("no cansado" -> positivo)
                
                if is_intensified:
                    val *= 1.5 # Aumentar impacto
                    
                score += val

        # Lógica de Decisión
        if score < -1:
            return -1, "Negativo Crítico (Bajando Intensidad)", "⚠️ Detecto fatiga o dolor. Bajando al mínimo. ¡Para si es necesario!"
        elif score < 0:
            return -1, "Negativo (Bajando Intensidad)", "Tranquilo, respira profundo. Bajamos la intensidad para que te recuperes. 🍃"
        elif score > 1:
            return 1, "Positivo Alto (Modo Bestia)", "¡MODO BESTIA ACTIVADO! 🦍🔥 ¡Nadie te para hoy!"
        elif score > 0:
            return 1, "Positivo (Subiendo Intensidad)", "¡Esa es la actitud! Subiendo la potencia. 🚀"
        else:
            return 0, "Neutral", "Estoy monitoreando. Dime 'estoy cansado' o 'vamos' para ajustar."
