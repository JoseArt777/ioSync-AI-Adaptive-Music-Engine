import requests
import json

def test_chatbot(message, heart_rate=100):
    url = "http://127.0.0.1:8000/recommend"
    payload = {
        "heart_rate": heart_rate,
        "current_song_id": None,
        "user_message": message,
        "hr_history": []
    }
    
    try:
        response = requests.post(url, json=payload)
        if response.status_code == 200:
            data = response.json()
            print(f"Message: '{message}'")
            print(f"Sentiment Analysis: {data.get('sentiment_analysis')}")
            print(f"Recommended Zone: {data.get('zone')}")
            print("-" * 30)
        else:
            print(f"Error: {response.status_code} - {response.text}")
    except Exception as e:
        print(f"Connection Error: {e}")

print("--- Verifying Chatbot Logic ---\n")

# Test 1: Neutral
test_chatbot(None)

# Test 2: Positive (Should boost intensity or keep it high)
test_chatbot("Me siento con mucha energía y felicidad")

# Test 3: Negative (Should lower intensity)
test_chatbot("Estoy muy cansado y agotado, necesito descansar")
