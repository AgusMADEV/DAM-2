# 🚀 Inicio Rápido - Sistema de Evacuación

## ⚡ Pasos para Ejecutar (5 minutos)

### 1️⃣ Requisitos Previos
- ✅ Navegador Chrome, Firefox o Edge actualizado
- ✅ Webcam conectada y funcionando
- ✅ Conexión a internet (para cargar librerías)

### 2️⃣ Ejecutar el Proyecto

**Opción A - Doble Clic (Más Simple)**
```
Haz doble clic en: index.html
```

**Opción B - Servidor Local (Recomendado)**
```bash
# Si tienes Python instalado:
python -m http.server 8000

# Luego abre en el navegador:
# http://localhost:8000
```

### 3️⃣ Primera Vez

1. El navegador pedirá acceso a la webcam → **ACEPTA**
2. Verás tu video en la esquina superior derecha
3. Muestra tu mano abierta frente a la cámara
4. Verás puntos verdes dibujados sobre tu mano ✅

### 4️⃣ Controlar la Cámara

**🎮 Prueba estos gestos:**

| Gesto | Instrucciones |
|-------|--------------|
| **Mover vista** | Una mano abierta → mueve lentamente |
| **Rotar** | Junta índice y pulgar (pinch) → mueve |
| **Zoom** | Dos manos abiertas → separa/junta |

### 5️⃣ Iniciar Simulación

1. Ajusta los sliders (personas, salidas)
2. Haz clic en **▶️ Iniciar Simulación**
3. Observa las cápsulas de colores evacuando
4. Mira las estadísticas en tiempo real

### 6️⃣ Ver Mapa de Calor

- Haz clic en **🔥 Mapa de Calor**
- Verás zonas rojas = congestión
- Útil para identificar problemas

---

## 🐛 Solución de Problemas

### ❌ "No detecta mis manos"
**Solución:**
- Asegúrate de tener buena iluminación
- Acerca más la mano a la cámara
- Abre bien los dedos
- Refresca la página (F5)

### ❌ "Pantalla negra en 3D"
**Solución:**
- Abre la consola (F12) y busca errores
- Verifica conexión a internet (carga Three.js de CDN)
- Prueba en Chrome (mejor soporte WebGL)

### ❌ "La webcam no funciona"
**Solución:**
- Verifica permisos del navegador (icono de cámara en barra de direcciones)
- Cierra otras apps que usen la webcam (Zoom, Teams, etc.)
- Prueba en modo incógnito

### ❌ "Va muy lento / se congela"
**Solución:**
- Reduce el número de personas (slider a 20-30)
- Cierra otras pestañas del navegador
- Actualiza drivers de tarjeta gráfica

---

## 🎯 Demo Rápida (1 minuto)

1. Abre `index.html`
2. Acepta webcam
3. Click en **▶️ Iniciar Simulación**
4. Observa durante 10 segundos
5. Click en **🔥 Mapa de Calor**
6. Mueve la vista con tu mano ✋
7. Click en **🔄 Reiniciar** para probar con diferentes configuraciones

---

## 📍 ¿Dónde Están los Archivos?

```
📁 002-Proyecto serious games/
  └── 📁 101-Ejercicios/
       ├── 📄 index.html          ← ABRE ESTE ARCHIVO
       ├── 📄 styles.css
       ├── 📄 README.md            ← Documentación completa
       ├── 📄 INICIO_RAPIDO.md     ← Este archivo
       └── 📁 scripts/
            ├── main.js
            ├── building.js
            ├── person.js
            ├── genetic-algorithm.js
            └── hand-controls.js
```

---

## 🎓 Para la Evaluación

**Demuestra estos puntos clave:**

1. ✅ **Tecnologías Multimedia Integradas**
   - Three.js (3D)
   - MediaPipe (IA)
   - Canvas (visualización)

2. ✅ **Algoritmo Genético Funcional**
   - Observa cómo mejoran los tiempos por generación
   - Abre consola (F12) para ver logs de evolución

3. ✅ **Control por Gestos**
   - Muestra los 3 tipos de gestos
   - Explica cómo funciona cada uno

4. ✅ **Aplicación Empresarial**
   - Explica el uso para seguridad laboral
   - Muestra el heat map y su utilidad
   - Configura diferentes escenarios (más/menos salidas)

---

## 💡 Tips para Impresionar

- 🎥 Activa el mapa de calor y muéstralo con la cámara
- 📊 Inicia varias generaciones y muestra la mejora de tiempos
- 🎮 Controla completamente con gestos (sin tocar mouse/teclado)
- 🔢 Prueba escenarios extremos (200 personas, 1 salida)
- 📝 Abre la consola para mostrar logs del algoritmo genético

---

## ❓ Preguntas Frecuentes

**P: ¿Funciona offline?**  
R: No, requiere internet para cargar Three.js y MediaPipe de CDN.

**P: ¿Puedo cambiar el edificio?**  
R: Sí, edita `building.js` y modifica `this.width` y `this.depth`.

**P: ¿Cuántas generaciones tarda en optimizar?**  
R: Entre 5-10 generaciones verás mejoras significativas.

**P: ¿Puedo exportar los datos?**  
R: No está implementado aún, pero sería una mejora futura.

**P: ¿Funciona en móvil?**  
R: La UI es responsive, pero los gestos están diseñados para pantalla grande.

---

## 🎉 ¡Listo!

Ya estás preparado para usar el sistema. Para documentación detallada, consulta [README.md](README.md).

**¡Disfruta explorando la simulación!** 🚨🏃‍♂️
