# 🎤 Guía de Presentación: BioSync AI

Este documento es una guía paso a paso para presentar el proyecto **BioSync AI**. Úsalo como guion durante tu demostración para explicar claramente el funcionamiento, la arquitectura y las decisiones de diseño (como la transición de música).

---

## 1. Introducción (El "Elevator Pitch")
**Objetivo:** Captar la atención en los primeros 30 segundos.

*   **Problema:** "Cuando hacemos ejercicio, a veces la música no encaja con nuestra energía. Una balada triste mientras corres a máxima velocidad te desmotiva."
*   **Solución:** "BioSync AI es un sistema inteligente que actúa como un DJ personal invisible. Escucha tu corazón (literalmente) y selecciona la música perfecta para mantenerte en tu zona de entrenamiento ideal."

---

## 2. Demostración en Vivo (El "Demo")
Sigue estos pasos en la interfaz mientras hablas:

### Paso 1: El Tablero (Dashboard)
*   **Acción:** Muestra la pantalla principal.
*   **Explicación:** "Esta es la interfaz de usuario. A la izquierda tenemos los controles de simulación y a la derecha la visualización en tiempo real."

### Paso 2: Simulación Manual
*   **Acción:** Mueve el slider de "Frecuencia Cardíaca" a **70 BPM** (Reposo).
*   **Explicación:** "Imaginemos que el usuario está calentando. El sistema detecta 70 BPM, lo clasifica en la **Zona Azul (Calentamiento)** y busca música tranquila (Bajo BPM, Baja Energía)."

### Paso 3: Aumentar la Intensidad
*   **Acción:** Sube el slider a **140 BPM** (Cardio).
*   **Explicación:** "Ahora el usuario empieza a correr. El sistema detecta el cambio de zona a **Naranja (Cardio)**. Fíjense como la música cambia a algo más rápido y energético para motivarlo."

### Paso 4: La "Magia" (Simulación Automática)
*   **Acción:** Activa el checkbox **"Simular Variación Automática"**.
*   **Explicación:** "En la vida real, el corazón no es estático. Aquí simulamos la lectura continua de un Smartwatch. El sistema monitorea cada segundo y ajusta la música dinámicamente."
*   **Visualización:** Señala la gráfica. "La línea roja es el usuario, la línea azul es la música intentando 'sincronizarse' con él."

---

## 3. Explicación Técnica (Arquitectura)
Si te preguntan "¿Cómo está hecho?", responde así:

*   **Frontend (Streamlit):** Lo que vemos. Se encarga de la visualización y de simular los sensores.
*   **Backend (FastAPI):** El "cerebro". Recibe los datos, ejecuta la lógica y devuelve la recomendación.
*   **Algoritmo:**
    1.  **Input:** Recibe BPM.
    2.  **Clasificación:** Determina la Zona (Quema Grasa, Cardio, Pico).
    3.  **Filtrado Vectorial:** Busca en la base de datos canciones que cumplan con el *Tempo* y *Energía* de esa zona.

---

## 4. Pregunta Clave: "¿Por qué la música cambia tan rápido?"
**Esta es la parte más importante para evitar confusiones.**

Es probable que alguien pregunte: *"¿No es molesto que la canción se corte a los 10 segundos?"*

**Tu Respuesta:**
> "Excelente observación. Lo que vemos aquí es un **prototipo diseñado para demostración**."

Explica estos dos puntos:

1.  **Compromiso de la Demo:**
    *   "Para esta presentación, he configurado el sistema para que cambie de canción cada **10 segundos**. Si esperáramos a que termine una canción real (3 minutos), tendríamos que estar aquí sentados mucho tiempo para ver un solo cambio. Queremos mostrar la capacidad de reacción del algoritmo."

2.  **Visión de Producto Real (Producción):**
    *   "En una aplicación comercial (como Spotify), el sistema usaría una **Cola Dinámica**. No cortaría la canción actual, sino que elegiría la *siguiente* canción en la lista basándose en tu ritmo cardiaco actual. Así la experiencia auditiva sería fluida y sin cortes."

---

## 5. Cierre
*   "BioSync AI demuestra cómo la complejidad algorítmica puede aplicarse a algo tan cotidiano como hacer ejercicio, mejorando el rendimiento y la motivación del usuario a través de la música."
