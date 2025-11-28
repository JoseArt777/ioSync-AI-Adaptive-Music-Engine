from BioSyncAI.backend.logic import BioSyncLogic

logic = BioSyncLogic()

def analyze_sentiment(message):
    return logic.analyze_sentiment(message)

# Test Cases
print("--- Probando Chatbot Centralizado (Logic.py) ---")
print(f"Input: 'Estoy muy cansado hoy' -> {analyze_sentiment('Estoy muy cansado hoy')}")
print(f"Input: 'Me siento con mucha energía' -> {analyze_sentiment('Me siento con mucha energía')}")
print(f"Input: 'Vamos con todo, me siento fuerte' -> {analyze_sentiment('Vamos con todo, me siento fuerte')}")
print(f"Input: 'Hola mundo' -> {analyze_sentiment('Hola mundo')}")
print(f"Input: 'Estoy agotado y muerto' -> {analyze_sentiment('Estoy agotado y muerto')}")
print(f"Input: 'No estoy cansado' -> {analyze_sentiment('No estoy cansado')}")
