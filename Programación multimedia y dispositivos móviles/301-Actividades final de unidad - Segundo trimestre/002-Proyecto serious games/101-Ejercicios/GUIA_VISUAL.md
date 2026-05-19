# 🎯 Guía Visual de Uso del Sistema

## 📺 Interfaz Principal

```
┌─────────────────────────────────────────────────────────────────┐
│ 🚨 Sistema de Entrenamiento de Evacuación                       │
│ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━│
│ Personas evacuadas: 45  │  Tiempo promedio: 12.3s  │  Gen: 3    │
└─────────────────────────────────────────────────────────────────┘

                    ┌─────────────────┐
                    │ 📹   WEBCAM     │
                    │                 │
                    │    👋 Manos     │
                    │   skeleton      │
                    ├─────────────────┤
                    │ 👋 Moviendo     │
                    │    cámara       │
                    └─────────────────┘

┌─────────────────────────────────────────────────────────────────┐
│                                                                   │
│                     🏢 EDIFICIO 3D                                │
│                                                                   │
│         🟢                                                🟢      │
│      ┌──────┐                                        ┌──────┐    │
│      │SALIDA│              🔴💡                       │SALIDA│    │
│      └──────┘                                        └──────┘    │
│                                                                   │
│            👤👤👤                                                 │
│                    🧱                                             │
│          👤           👤                                          │
│              👤                    🧱                             │
│                  👤👤                                             │
│                          👤                                       │
│                                                                   │
│         🟢                                                🟢      │
│      ┌──────┐                                        ┌──────┐    │
│      │SALIDA│                                        │SALIDA│    │
│      └──────┘                                        └──────┘    │
│                                                                   │
└─────────────────────────────────────────────────────────────────┘

┌──────────────────────┐              ┌──────────────────────────┐
│ ⚙️  Configuración    │              │ 🎮 Controles por Gestos   │
│ ───────────────────  │              │ ─────────────────────────│
│                      │              │                          │
│ Personas: [▓▓▓░] 50  │              │ ✋ Palma abierta + Mover │
│ Salidas:  [▓▓░ ] 2   │              │    → Mover cámara        │
│ Velocidad:[▓▓▓▓] 5   │              │                          │
│                      │              │ 🤏 Índice + Pulgar       │
│ [▶️  Iniciar Sim.]   │              │    → Rotar cámara        │
│ [🔄  Reiniciar   ]   │              │                          │
│ [🔥  Mapa Calor  ]   │              │ ✌️  Dos manos abiertas   │
│                      │              │    → Zoom                │
└──────────────────────┘              └──────────────────────────┘
```

---

## 🎨 Estados Visuales

### 1️⃣ Estado Inicial (Sin simulación)

```
📊 Estadísticas: Evacuados: 0 | Tiempo: 0s | Generación: 1
🏢 Edificio: Vacío, con salidas señalizadas
🎮 Botón: "▶️ Iniciar Simulación" (verde)
📹 Webcam: Activa, esperando manos
```

### 2️⃣ Simulación en Curso

```
📊 Estadísticas: Actualización en tiempo real
🏢 Edificio: Personas moviéndose (cápsulas de colores)
🎮 Botón: "⏸️ Pausar Simulación" (rojo)
💡 Luces: Parpadeo de emergencia
👥 Personas: Animación de caminar hacia salidas
```

### 3️⃣ Con Mapa de Calor Activo

```
🔥 Overlay: Gradiente de calor visible en el suelo
   🟢 Verde: Baja densidad (0-2 personas)
   🟡 Amarillo: Densidad media (3-4 personas)
   🔴 Rojo: Alta densidad (5+ personas)
🎯 Utilidad: Identificar zonas congestionadas
```

---

## 👋 Gestos Paso a Paso

### Gesto 1: Mover Cámara (PAN)

```
Paso 1: Extiende UNA mano frente a la cámara
        
        📹 [   👋  ]
        
Paso 2: Abre completamente los dedos

        📹 [   🖐️  ]
        
Paso 3: Mueve la mano lentamente

        📹 [ 🖐️ →  ] → Cámara se mueve a la derecha
        📹 [ ← 🖐️ ] → Cámara se mueve a la izquierda
        
Resultado: Vista se desplaza lateralmente
```

### Gesto 2: Rotar Cámara (ROTATE)

```
Paso 1: Junta índice y pulgar (pinch)

        📹 [   🤏  ]
        
Paso 2: Mantén el pinch

        📹 [   🤏  ] ✅ Detectado
        
Paso 3: Mueve la mano horizontalmente

        📹 [ → 🤏  ] → Cámara rota en sentido horario
        📹 [ 🤏 ← ] → Cámara rota antihorario
        
Resultado: Vista orbital alrededor del edificio
```

### Gesto 3: Zoom (ZOOM)

```
Paso 1: Extiende AMBAS manos

        📹 [ 🖐️    🖐️ ]
        
Paso 2: Abre completamente

        📹 [ 🖐️    🖐️ ] ✅ Detectadas
        
Paso 3: Separa/Junta las manos

        📹 [ 🖐️  ←→  🖐️ ] → Zoom out (alejar)
        📹 [ 🖐️  →←  🖐️ ] → Zoom in (acercar)
        
Resultado: Cámara se aleja/acerca
```

---

## 📈 Flujo de Trabajo Típico

### Escenario A: Prueba Rápida (2 minutos)

```
1. Abre index.html
2. Acepta webcam
3. [▶️ Iniciar Simulación]
4. Observa 30 segundos
5. Prueba gestos:
   - ✋ Mover vista
   - 🤏 Rotar
   - ✌️ Zoom
6. [🔥 Mapa de Calor]
7. Identifica zonas rojas
```

### Escenario B: Análisis Completo (10 minutos)

```
1. Configurar parámetros:
   - Personas: 100
   - Salidas: 2
   
2. [▶️ Iniciar Simulación]

3. Observar primera generación completa
   - Anotar tiempo promedio inicial
   
4. Dejar evolucionar 5 generaciones
   - Generación 1: ~15s promedio
   - Generación 2: ~13s promedio
   - Generación 3: ~11s promedio
   - Generación 4: ~10s promedio
   - Generación 5: ~9s promedio
   
5. [🔄 Reiniciar]

6. Cambiar configuración:
   - Personas: 100
   - Salidas: 4 (2 más)
   
7. Repetir y comparar tiempos
   - ¿Mejora con más salidas?
   
8. [🔥 Mapa de Calor]
   - Identificar puntos críticos
```

### Escenario C: Demostración Educativa (5 minutos)

```
1. Explicar el problema:
   "Empresas deben cumplir normativas de evacuación"
   
2. Mostrar interfaz:
   "Sistema interactivo 3D con IA"
   
3. Configurar escenario extremo:
   - Personas: 200
   - Salidas: 1
   
4. [▶️ Iniciar]
   "Observen el cuello de botella en la única salida"
   
5. [🔥 Mapa de Calor]
   "La zona roja indica congestión peligrosa"
   
6. [🔄 Reiniciar] + Cambiar a 3 salidas
   
7. Comparar:
   "Con 3 salidas, el tiempo se reduce un 65%"
   
8. Mostrar gestos:
   - ✋ Control sin tocar nada
   - Rotar para ver diferentes ángulos
```

---

## 🎯 Indicadores Visuales de Estado

### Colores de las Personas

```
🟢 Verde claro:   Poco pánico (comportamiento racional)
🟡 Verde-amarillo: Pánico medio
🟠 Naranja:        Pánico alto (movimientos erráticos)
```

### Luces del Edificio

```
🔴 Roja parpadeante: Luz de emergencia (parpadea cada 50ms)
🟢 Verde estática:   Salida de emergencia
⚪ Blanca difusa:    Iluminación ambiente
```

### Indicador de Gesto Activo

```
🟩 Verde:   "👋 Moviendo cámara" (Pan)
🟦 Azul:    "🤏 Rotando cámara" (Rotate)
🟧 Naranja: "✌️ Zoom" (Zoom)
⬜ Gris:    "👋 Muestra tus manos" (Idle)
🟥 Rojo:    "❌ Error de webcam" (Error)
```

---

## 🧪 Casos de Prueba

### Prueba 1: Convergencia del Algoritmo Genético

```
Configuración:
- Personas: 50
- Salidas: 2
- Velocidad: 5

Esperado:
✅ Generación 1: ~12-15s promedio
✅ Generación 3: ~10-12s promedio
✅ Generación 5: ~8-10s promedio
✅ Generación 10: ~7-9s promedio (convergencia)

Cómo verificar:
1. Observa el panel de estadísticas
2. Anota "Tiempo promedio" cada generación
3. Abre consola (F12), verás logs:
   🧬 Evolucionando generación X...
   📊 Mejor: Xs | Promedio: Ys | Peor: Zs
```

### Prueba 2: Escalabilidad

```
Configuración:
- Personas: 10 → 50 → 100 → 200
- Salidas: 2
- Observar FPS

Esperado:
✅ 10 personas:  60 FPS
✅ 50 personas:  60 FPS
✅ 100 personas: 50-60 FPS
✅ 200 personas: 45-55 FPS

Cómo verificar:
- Observa fluidez visual
- Si se congela: reduce personas
```

### Prueba 3: Detección de Gestos

```
Configuración:
- Luz ambiente: Buena iluminación
- Distancia webcam: 50-80cm
- Fondo: Uniforme (mejor contraste)

Gestos a probar:
1. ✋ Una mano abierta → Debería decir "Moviendo cámara"
2. 🤏 Pinch → Debería decir "Rotando cámara"
3. ✌️ Dos manos → Debería decir "Zoom"

Esperado:
✅ Detección en <100ms
✅ Skeleton verde sobre manos
✅ Cambio de indicador de texto
✅ Movimiento de cámara visible

Si falla:
- Mejora iluminación
- Acerca más la mano
- Abre completamente los dedos
```

---

## 🎬 Secuencia de Demo Completa (Para Evaluación)

```
┌──────────────────────────────────────────────────┐
│ GUIÓN DE DEMOSTRACIÓN (5 minutos)                │
├──────────────────────────────────────────────────┤
│                                                   │
│ [0:00-0:30] Introducción                         │
│   - "Sistema de evacuación empresarial"          │
│   - "Combina 3D, IA y vision por computadora"    │
│                                                   │
│ [0:30-1:00] Mostrar Interfaz                     │
│   - Recorrer paneles con gestos                  │
│   - Explicar cada sección                        │
│                                                   │
│ [1:00-2:00] Iniciar Simulación                  │
│   - Configurar: 50 personas, 2 salidas           │
│   - [▶️ Iniciar]                                 │
│   - Explicar qué ocurre en pantalla              │
│                                                   │
│ [2:00-3:00] Demostrar Gestos                     │
│   - ✋ Mover cámara                               │
│   - 🤏 Rotar vista                                │
│   - ✌️ Hacer zoom                                │
│   - Mostrar skeleton en webcam                   │
│                                                   │
│ [3:00-3:30] Algoritmo Genético                   │
│   - Esperar a generación 2-3                     │
│   - Mostrar mejora de tiempos                    │
│   - Abrir consola → logs de evolución            │
│                                                   │
│ [3:30-4:00] Heat Map                             │
│   - [🔥 Activar]                                 │
│   - Explicar zonas rojas = congestión            │
│   - Aplicación empresarial                       │
│                                                   │
│ [4:00-4:30] Configuración Avanzada               │
│   - Cambiar a 4 salidas                          │
│   - [🔄 Reiniciar]                               │
│   - Comparar tiempos                             │
│                                                   │
│ [4:30-5:00] Conclusión                           │
│   - Resumen de tecnologías                       │
│   - Aplicación real (PRL, arquitectura)          │
│   - Preguntas                                    │
│                                                   │
└──────────────────────────────────────────────────┘
```

---

## 📸 Puntos Fotográficos Clave

Si necesitas capturas de pantalla para documentación:

1. **Interfaz completa** (vista general)
2. **Panel de webcam** con skeleton visible
3. **Edificio 3D** desde arrarriba (vista cenital)
4. **Personas evacuando** en movimiento
5. **Heat map activo** con zonas rojas
6. **Consola** con logs de algoritmo genético
7. **Panel de estadísticas** con valores altos
8. **Gestos** (foto de tu mano + indicador en pantalla)

---

**¡Listo para usar!** 🎉

Para cualquier duda, consulta [README.md](README.md) o [INICIO_RAPIDO.md](INICIO_RAPIDO.md)
