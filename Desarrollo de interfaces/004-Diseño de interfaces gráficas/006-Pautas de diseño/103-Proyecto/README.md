# 🎮 Simulación de Partículas 3D con Física Interactiva

## 🌟 Descripción

Proyecto interactivo que implementa un **sistema avanzado de partículas en 3D** con física realista. Diseñado para aprender y experimentar con conceptos de física mediante simulaciones visuales en tiempo real.

![Versión](https://img.shields.io/badge/version-1.0-blue)
![A-Frame](https://img.shields.io/badge/A--Frame-1.5.0-orange)
![Licencia](https://img.shields.io/badge/license-Educational-green)

---

## ✨ Características Principales

- 🎬 **6 Escenarios Predefinidos**: Lluvia, Explosión, Fuente, Sistema Orbital, Vórtice, Caos
- ⚛️ **Física Realista**: Gravedad, fricción, colisiones elásticas, fuerzas centrípetas
- 🎮 **Controles en Tiempo Real**: Modifica parámetros físicos mientras la simulación corre
- 🎨 **Efectos Visuales**: Colores dinámicos, emisividad, iluminación avanzada
- 📊 **Estadísticas en Vivo**: FPS, contador de partículas
- 🖱️ **Interacción**: Click para crear explosiones localizadas
- 📐 **Hasta 500 partículas** simultáneas con detección de colisiones

---

## 🚀 Inicio Rápido

### Opción 1: Ejecutar Directamente
```bash
# Simplemente abre el archivo en tu navegador
simulacion-particulas.html
```

### Opción 2: Con Servidor Local
```bash
# Si tienes Python instalado
python -m http.server 8000

# O con Node.js (usando http-server)
npx http-server

# Luego abre: http://localhost:8000/simulacion-particulas.html
```

### Requisitos
- Navegador moderno (Chrome, Firefox, Edge, Safari)
- WebGL habilitado
- Tarjeta gráfica compatible con aceleración 3D

---

## 📂 Estructura del Proyecto

```
102-Actividad EVAL/
├── simulacion-particulas.html    # ⭐ Archivo principal (ABRIR ESTE)
├── README.md                       # Este archivo
├── DOCUMENTACION.md                # Documentación técnica completa
└── GUIA-EXPERIMENTOS.md            # Guía de 10 experimentos prácticos
```

---

## 🎮 Controles

### Navegación 3D
| Tecla/Acción | Función |
|--------------|---------|
| **W/S** | Avanzar / Retroceder |
| **A/D** | Izquierda / Derecha |
| **Q/E** | Subir / Bajar |
| **Ratón** | Mirar alrededor (arrastra) |
| **Click** | Crear explosión en dirección de la mirada |

### Panel de Control
- **Escenarios**: 6 botones para cargar configuraciones predefinidas
- **Partículas**: Ajusta cantidad (50-500) y regenera
- **Fuerzas**: Gravedad, viento (X/Z), fuerza central
- **Propiedades**: Fricción, rebote, radio de partículas
- **Efectos**: Estelas, colores dinámicos, colisiones
- **Simulación**: Pausar, reiniciar, limpiar

---

## 🎬 Los 6 Escenarios

### 1. 🌧️ Lluvia
Simula caída de gotas con gravedad fuerte y bajo rebote.  
**Para aprender**: Caída libre, rebotes, resistencia del aire

### 2. 💥 Explosión
Expansión radial simétrica desde el centro.  
**Para aprender**: Distribución de velocidades, simetría esférica

### 3. ⛲ Fuente
Generación continua de partículas con trayectoria parabólica.  
**Para aprender**: Movimiento parabólico, generación dinámica

### 4. 🛸 Sistema Orbital
Partículas orbitando alrededor de un punto central.  
**Para aprender**: Fuerza centrípeta, órbitas, velocidad angular

### 5. 🌪️ Vórtice
Espiral descendente con rotación.  
**Para aprender**: Movimiento circular, combinación de fuerzas

### 6. 🎲 Caos
Parámetros totalmente aleatorios en cada ejecución.  
**Para aprender**: Teoría del caos, sensibilidad a condiciones iniciales

---

## 🔬 Conceptos Físicos Implementados

### Cinemática
- Posición, velocidad y aceleración en 3D
- Integración numérica (Euler)
- Límites espaciales con rebotes

### Dinámica
- **Gravedad**: Aceleración constante hacia abajo
- **Viento**: Fuerzas horizontales constantes
- **Fuerza Central**: Atracción hacia un punto (centrípeta)
- **Fricción**: Disipación de energía proporcional a velocidad

### Colisiones
- **Con límites**: Rebotes con coeficiente de restitución
- **Entre partículas**: Colisiones elásticas simplificadas
- Conservación de momento (aproximada)

---

## 📚 Documentación

### Para Empezar
1. Lee este **README.md** (visión general)
2. Abre **simulacion-particulas.html** y prueba los escenarios
3. Sigue la **GUIA-EXPERIMENTOS.md** (10 experimentos paso a paso)

### Para Profundizar
4. Lee la **DOCUMENTACION.md** completa:
   - Conceptos físicos detallados
   - Ecuaciones matemáticas
   - Arquitectura del código
   - Optimizaciones y mejoras posibles
   - Recursos de aprendizaje

---

## 🧪 Experimentos Sugeridos

### Nivel Básico ⭐
1. **Gravedad lunar**: Reduce gravedad a -0.003
2. **Mundo sin fricción**: Fricción = 0.999
3. **Rebotes extremos**: Rebote = 0 vs 1

### Nivel Intermedio ⭐⭐
4. **Agujero negro**: Fuerza central al máximo
5. **Huracán artificial**: Combina viento + fuerza central
6. **Fuente con viento**: Observa trayectorias inclinadas

### Nivel Avanzado ⭐⭐⭐
7. **Órbita perfecta**: Ajusta parámetros para órbitas circulares
8. **Sistema solar**: Múltiples órbitas estables
9. **Anti-gravedad**: Gravedad positiva

Consulta **GUIA-EXPERIMENTOS.md** para instrucciones detalladas.

---

## 🛠️ Tecnologías Utilizadas

- **[A-Frame 1.5.0](https://aframe.io)**: Framework de VR/3D para la web
- **[Three.js](https://threejs.org)**: Motor 3D subyacente
- **JavaScript ES6+**: Lógica de simulación
- **WebGL**: Renderizado acelerado por GPU
- **HTML5/CSS3**: Interfaz y controles

---

## 📊 Parámetros Físicos

| Parámetro | Rango | Unidad | Descripción |
|-----------|-------|--------|-------------|
| Gravedad | -0.05 a +0.05 | m/s² | Aceleración vertical |
| Viento X/Z | -0.02 a +0.02 | m/s² | Fuerzas horizontales |
| Fuerza Central | 0 a 0.005 | m/s² | Atracción al centro |
| Fricción | 0.8 a 0.999 | - | Factor de desaceleración |
| Rebote | 0 a 1 | - | Coeficiente de restitución |
| Radio | 0.1 a 0.5 | m | Tamaño de partículas |
| Cantidad | 50 a 500 | - | Número de partículas |

---

## 🎯 Objetivos de Aprendizaje

Al usar este proyecto, aprenderás:

### Física
- ✅ Mecánica newtoniana (F = ma)
- ✅ Cinemática en 3D
- ✅ Colisiones y conservación de momento
- ✅ Movimiento orbital
- ✅ Disipación de energía

### Programación
- ✅ Programación orientada a objetos
- ✅ Bucles de animación
- ✅ Integración numérica
- ✅ Detección de colisiones
- ✅ Optimización de rendimiento

### Gráficos 3D
- ✅ Sistemas de coordenadas 3D
- ✅ Renderizado en tiempo real
- ✅ Iluminación dinámica
- ✅ Sistemas de partículas

---

## 🔄 Modificaciones vs. Ejemplos de Clase

Este proyecto está basado en los ejercicios **005, 006, 007, 008** de la carpeta `101-Ejercicios`, con estas mejoras:

### ➕ Añadido (nuevo)
- 6 escenarios predefinidos completos
- Fuerza central/centrípeta
- Viento en dos ejes
- Colisiones entre partículas
- Sistema de vida útil
- Generación continua (Fuente)
- Click interactivo para explosiones
- Estadísticas en vivo (FPS, contador)

### 🔧 Mejorado
- Controles más completos e intuitivos
- Interfaz visual moderna
- Mejor iluminación y efectos
- Código más estructurado y documentado
- Rangos de parámetros optimizados

### ✅ Mantenido
- Sistema de coordenadas 3D
- Física base (velocidad, aceleración)
- Navegación WASD + QE
- Rebotes con límites

---

## 💡 Ideas para Extensiones

¿Quieres llevar el proyecto más allá?

### Fácil ⭐
- Añadir más colores de partículas
- Crear tu propio escenario personalizado
- Cambiar el diseño de la interfaz

### Medio ⭐⭐
- Implementar nuevos tipos de fuerzas
- Añadir export/import de configuraciones
- Crear modo editor visual

### Difícil ⭐⭐⭐
- Simulación de fluidos (SPH)
- Partículas con carga eléctrica
- Optimización con Spatial Hashing
- VR/AR con controladores

---

## 🐛 Solución de Problemas

### Problema: Bajo rendimiento (FPS < 30)
**Soluciones**:
- Reduce número de partículas a 100-150
- Desactiva colisiones entre partículas
- Desactiva estelas
- Cierra otras pestañas

### Problema: Las partículas "explotan" (velocidades infinitas)
**Causa**: Fuerzas demasiado altas o dt muy grande  
**Solución**: Reduce valores de fuerzas, aumenta fricción

### Problema: No se ve nada
**Soluciones**:
- Verifica consola del navegador (F12)
- Navega hacia el centro (0, 10, 0)
- Regenera partículas
- Prueba otro navegador

### Problema: Navegación muy lenta/rápida
**Solución**: Modifica `velocidadVuelo` en el código (línea ~680)

---

## 📖 Recursos Adicionales

### Aprender Más Física
- [Khan Academy - Physics](https://www.khanacademy.org/science/physics)
- [The Physics Classroom](https://www.physicsclassroom.com/)
- [3Blue1Brown - Essence of Calculus](https://www.youtube.com/playlist?list=PLZHQObOWTQDMsr9K-rj53DwVRMYO3t5Yr)

### Aprender A-Frame y Three.js
- [A-Frame School](https://aframe.io/aframe-school/)
- [A-Frame Documentation](https://aframe.io/docs/)
- [Three.js Journey](https://threejs-journey.com/)
- [Three.js Fundamentals](https://threejsfundamentals.org/)

### Programación de Juegos y Física
- [Game Programming Patterns](https://gameprogrammingpatterns.com/)
- [Nature of Code](https://natureofcode.com/) - Daniel Shiffman
- [The Coding Train](https://www.youtube.com/c/TheCodingTrain) (YouTube)

---

## 👨‍🎓 Información Académica

**Curso**: Desarrollo de Interfaces Gráficas  
**Nivel**: DAM-2 (Desarrollo de Aplicaciones Multiplataforma)  
**Tema**: Física 3D y Simulación de Partículas  
**Basado en**: Ejercicios de la carpeta `101-Ejercicios`  
**Fecha**: 8 de febrero de 2026

---

## 📝 Licencia

Proyecto educativo de código abierto.  
Libre para usar, modificar y aprender.

---

## 🙏 Agradecimientos

- **A-Frame Team** por el excelente framework
- **Three.js Community** por el motor 3D
- **Profesores del curso** por los ejemplos base
- **Daniel Shiffman (The Coding Train)** por la inspiración

---

## 📞 Soporte

Si tienes dudas:
1. Consulta la **DOCUMENTACION.md**
2. Revisa la **GUIA-EXPERIMENTOS.md**
3. Pregunta al profesor
4. Comunidad de [A-Frame](https://aframe.io/community/)
5. Foros de [Three.js](https://discourse.threejs.org/)

---

## 🎓 Evaluación Sugerida

Si este es un proyecto para evaluar, considera:

### Comprensión Teórica (40%)
- ✅ Explica 3 conceptos físicos implementados
- ✅ Describe cómo funcionan las colisiones
- ✅ Identifica las fuerzas en cada escenario

### Experimentación Práctica (30%)
- ✅ Completa al menos 5 experimentos de la guía
- ✅ Documenta observaciones
- ✅ Responde preguntas teóricas

### Modificación del Código (30%)
- ✅ Crea un escenario personalizado
- ✅ Modifica un parámetro físico
- ✅ Añade un efecto visual

---

## 🚀 Próximos Pasos

1. **Explora**: Prueba todos los escenarios
2. **Experimenta**: Sigue la guía de experimentos
3. **Aprende**: Lee la documentación completa
4. **Modifica**: Cambia el código y crea algo nuevo
5. **Comparte**: Muestra tus descubrimientos

---

<div align="center">

### ⭐ ¡Diviértete y Aprende! ⭐

**"La física no es solo ecuaciones, es entender cómo funciona el universo"**

[🎮 Abrir Simulación](simulacion-particulas.html) | [📖 Documentación](DOCUMENTACION.md) | [🧪 Experimentos](GUIA-EXPERIMENTOS.md)

---

*Proyecto creado con ❤️ para aprender física de forma interactiva*

</div>
