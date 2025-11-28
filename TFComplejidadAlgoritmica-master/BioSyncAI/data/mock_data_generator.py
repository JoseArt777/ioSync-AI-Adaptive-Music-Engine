import pandas as pd
import numpy as np
import random

def generate_mock_spotify_data(num_tracks=1000):
    """Generates a mock dataset resembling the Spotify Tracks Dataset."""
    genres = ['Pop', 'Rock', 'EDM', 'Hip-Hop', 'Jazz', 'Classical', 'Indie', 'Metal']
    data = []
    
    for i in range(num_tracks):
        genre = random.choice(genres)
        
        # Correlate energy and tempo roughly with genre for realism
        if genre in ['EDM', 'Metal', 'Rock']:
            base_energy = 0.7
            base_tempo = 120
        elif genre in ['Pop', 'Hip-Hop']:
            base_energy = 0.5
            base_tempo = 100
        else: # Jazz, Classical, Indie
            base_energy = 0.3
            base_tempo = 80
            
        energy = min(1.0, max(0.0, np.random.normal(base_energy, 0.15)))
        tempo = max(60, np.random.normal(base_tempo, 20))
        valence = random.random() # Mood
        
        data.append({
            'track_id': f'track_{i}',
            'track_name': f'Song {i}',
            'artists': f'Artist {random.randint(1, 100)}',
            'genre': genre,
            'tempo': round(tempo, 1),
            'energy': round(energy, 2),
            'valence': round(valence, 2),
            'danceability': round(random.random(), 2)
        })
        
    df = pd.DataFrame(data)
    return df

if __name__ == "__main__":
    print("Generating mock Spotify data...")
    df = generate_mock_spotify_data()
    df.to_csv("spotify_mock.csv", index=False)
    print("Saved to spotify_mock.csv")
