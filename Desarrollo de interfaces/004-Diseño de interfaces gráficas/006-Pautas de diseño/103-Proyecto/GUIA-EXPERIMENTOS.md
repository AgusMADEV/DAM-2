# 🚀 Simulación de Partículas 3D - Guía Rápida

## 📂 Contenido del Proyecto

Este proyecto contiene:

1. **simulacion-particulas.html** - La simulación interactiva (archivo principal)
2. **DOCUMENTACION.md** - Documentación completa con teoría física
3. **GUIA-EXPERIMENTOS.md** - Esta guía de experimentos prácticos
4. **README.md** - Resumen general del proyecto

---

## ⚡ Inicio Rápido

1. Abre `simulacion-particulas.html` en tu navegador
2. Haz click en cualquier escenario (recomendado: **Explosión** o **Sistema Orbital**)
3. Usa WASD + QE + Ratón para navegar
4. Experimenta con los controles deslizantes

---

## 🎬 Los 6 Escenarios Explicados

### 1. 🌧️ Lluvia
**¿Qué hace?** Caída de partículas como gotas de lluvia  
**Lo mejor para aprender**: Gravedad y rebotes  
**Prueba esto**: Cambia el coeficiente de rebote a 0.8 y verás las gotas "rebotando" más

### 2. 💥 Explosión
**¿Qué hace?** Expansión radial desde el centro  
**Lo mejor para aprender**: Distribución de velocidades  
**Prueba esto**: Justo después de la explosión, ponla en pausa y observa la simetría

### 3. ⛲ Fuente
**¿Qué hace?** Chorro continuo de partículas hacia arriba  
**Lo mejor para aprender**: Trayectorias parabólicas  
**Prueba esto**: Añade viento X = 0.01 y ve cómo se desvía la fuente

### 4. 🛸 Sistema Orbital
**¿Qué hace?** Partículas orbitando un punto central  
**Lo mejor para aprender**: Fuerza centrípeta y órbitas  
**Prueba esto**: Aumenta la fuerza central hasta 0.004 y observa órbitas más cerradas

### 5. 🌪️ Vórtice
**¿Qué hace?** Espiral descendente  
**Lo mejor para aprender**: Movimiento circular combinado  
**Prueba esto**: Quita la gravedad (0) y tendrás un disco giratorio plano

### 6. 🎲 Caos
**¿Qué hace?** Parámetros aleatorios cada vez  
**Lo mejor para aprender**: Cómo pequeños cambios generan grandes diferencias  
**Prueba esto**: Ejecuta 5 veces seguidas y compara los patrones

---

## 🧪 10 Experimentos Prácticos Paso a Paso

### Experimento 1: La Gravedad en la Luna 🌙
**Tiempo**: 2 minutos  
**Dificultad**: ⭐

1. Escenario: **Lluvia**
2. Cambia Gravedad a: `-0.003` (1/6 de la Tierra)
3. Observa: Las gotas caen mucho más lento

**Pregunta**: ¿Cómo sería jugar al baloncesto en la Luna?

---

### Experimento 2: Mundo sin Fricción 🧊
**Tiempo**: 3 minutos  
**Dificultad**: ⭐

1. Escenario: **Explosión**
2. Pon Fricción a: `0.999` (casi sin fricción)
3. Observa: Las partículas se mueven casi eternamente

**Compara**: Ahora pon fricción a `0.85` (mucha fricción)

**Pregunta**: ¿Qué representa la fricción? (Aire, agua, etc.)

---

### Experimento 3: Rebote de Pelota vs. Plastilina 🏀
**Tiempo**: 2 minutos  
**Dificultad**: ⭐

1. Escenario: **Lluvia**
2. Primera prueba: Coef. Rebote = `0.9` (pelota de goma)
3. Segunda prueba: Coef. Rebote = `0.1` (plastilina)

**Observa**: Cuántos rebotes da cada una

**Pregunta**: ¿Qué objetos reales tienen rebote cercano a 1? ¿Y a 0?

---

### Experimento 4: Agujero Negro en el Centro 🕳️
**Tiempo**: 3 minutos  
**Dificultad**: ⭐⭐

1. Escenario: **Sistema Orbital**
2. Aumenta Fuerza Central a: `0.005` (máximo)
3. Observa: Las partículas son "tragadas" hacia el centro
4. Opcional: Pon Gravedad a 0 para ver mejor el efecto

**Pregunta**: ¿Por qué no escapan las partículas?

---

### Experimento 5: Cohete en Gravedad Cero 🚀
**Tiempo**: 4 minutos  
**Dificultad**: ⭐⭐

1. Escenario: **Caos** (varias veces hasta conseguir gravedad cerca de 0)
2. O manualmente: Gravedad = `0`, Viento = `0`, Fricción = `0.999`
3. Click en el espacio para crear "propulsión"
4. Observa: Primera Ley de Newton en acción

**Pregunta**: ¿Por qué un objeto en el espacio sigue moviéndose sin motores?

---

### Experimento 6: Huracán Artificial 🌀
**Tiempo**: 5 minutos  
**Dificultad**: ⭐⭐⭐

**Objetivo**: Crear un huracán realista

1. Escenario: Cualquiera → Limpiar
2. Configura:
   - Gravedad: `-0.002`
   - Viento X: `0.008`
   - Viento Z: `0.008`
   - Fuerza Central: `0.0015`
   - Fricción: `0.992`
3. Regenerar 300 partículas
4. Observa: Espiral con ojo central

**Pregunta**: ¿Qué crea el "ojo" del huracán?

---

### Experimento 7: Fuente con Viento Lateral 💨
**Tiempo**: 3 minutos  
**Dificultad**: ⭐⭐

1. Escenario: **Fuente**
2. Espera a que se llene
3. Añade Viento X: `0.015`
4. Observa: La parábola se inclina

**Extra**: Prueba con Viento Z para ver el efecto en 3D

**Pregunta**: ¿Cómo afecta el viento a una fuente real?

---

### Experimento 8: Detectar la Órbita Perfecta ⭕
**Tiempo**: 5 minutos  
**Dificultad**: ⭐⭐⭐

**Objetivo**: Conseguir órbitas circulares perfectas y estables

1. Escenario: **Sistema Orbital**
2. Ajusta Fricción a: `0.999`
3. Ajusta Fuerza Central hasta ver órbitas circulares (prueba `0.0018`)
4. Pausa y observa

**Bonus**: Busca la relación entre radio y velocidad orbital

**Pregunta**: ¿Por qué órbitas más alejadas parecen más lentas?

---

### Experimento 9: Gravedad Invertida (Anti-gravedad) ⬆️
**Tiempo**: 3 minutos  
**Dificultad**: ⭐⭐

1. Escenario: **Lluvia**
2. Cambia Gravedad a: `+0.02` (positiva, hacia arriba)
3. Observa: Las partículas "caen" hacia arriba
4. Espera: Se acumulan en el techo

**Pregunta**: ¿Podría existir anti-gravedad en la realidad?

---

### Experimento 10: Crear un Géiser de Júpiter 🪐
**Tiempo**: 6 minutos  
**Dificultad**: ⭐⭐⭐⭐

**Objetivo**: Simular los géiseres de la luna Europa

1. Empezar de cero (Limpiar)
2. Configurar:
   - Num. Partículas: `150`
   - Gravedad: `-0.025` (Júpiter tiene más gravedad)
   - Fricción: `0.996`
   - Rebote: `0.2`
   - Fuerza Central: `0`
3. Regenerar
4. Las partículas deben salir del suelo y caer rápido

**Tweaking**: Ajusta gravedad hasta conseguir el efecto deseado

**Pregunta**: ¿Cómo cambia la trayectoria con mayor gravedad?

---

## 🎯 Desafíos Avanzados

### Desafío 1: Réplica del Sistema Solar 🌍☀️
**Dificultad**: ⭐⭐⭐⭐

Configura parámetros para que:
- Haya un "sol" central (esfera roja ya existe)
- Las partículas orbiten a diferentes distancias
- Las órbitas sean estables durante al menos 1 minuto

**Pista**: Necesitas gravedad ~0, alta fricción, y fuerza central precisa

---

### Desafío 2: Efecto Domino de Colisiones ⚫⚫⚫
**Dificultad**: ⭐⭐⭐⭐

1. Coloca pocas partículas (50)
2. Alta velocidad inicial
3. Activa colisiones
4. Observa reacciones en cadena

**Objetivo**: Crear una "reacción en cadena" visible

---

### Desafío 3: Recrear el Experimento de Galileo 🏛️
**Dificultad**: ⭐⭐⭐

Galileo demostró que objetos de distinta masa caen igual en vacío.

1. Escenario personalizado:
   - Gravedad: `-0.015`
   - Fricción: `0.999` (vacío)
   - Rebote: `0`
2. Todas las partículas deberían caer igual

**Pregunta**: ¿Qué pasaría con fricción baja (aire)?

---

## 📊 Tabla de Valores Recomendados por Efecto

| Efecto Deseado | Gravedad | Fricción | Rebote | Fuerza Central |
|----------------|----------|----------|--------|----------------|
| **Lluvia suave** | -0.008 | 0.996 | 0.1 | 0 |
| **Nieve** | -0.003 | 0.990 | 0.05 | 0 |
| **Pelota botando** | -0.015 | 0.985 | 0.85 | 0 |
| **Fuegos artificiales** | -0.010 | 0.980 | 0.4 | 0 |
| **Satélites** | 0 | 0.999 | 0.9 | 0.0020 |
| **Tornado** | -0.004 | 0.993 | 0.3 | 0.0012 |
| **Cascada** | -0.020 | 0.997 | 0.2 | 0 |

---

## 🔬 Observaciones Científicas a Realizar

Mientras experimentas, intenta responder:

### Sobre Gravedad:
- ¿Cómo afecta la gravedad al tiempo de caída?
- ¿A qué velocidad máxima llegan las partículas?
- ¿Qué pasa con gravedad = 0?

### Sobre Fricción:
- ¿Cuánto tarda una partícula en detenerse?
- ¿La fricción es proporcional a la velocidad?
- ¿Qué representa en el mundo real?

### Sobre Colisiones:
- ¿Se conserva la energía en las colisiones?
- ¿Qué pasa con el momento total del sistema?
- ¿Por qué algunas partículas se "quedan pegadas"?

### Sobre Órbitas:
- ¿Cuál es la relación entre fuerza central y radio orbital?
- ¿Por qué algunas órbitas son circulares y otras elípticas?
- ¿Qué pasa si la velocidad inicial es muy alta/baja?

---

## 💡 Tips y Trucos

### 🎥 Para Mejores Visualizaciones:
1. **Cámara lenta**: Aumenta fricción a 0.999
2. **Zoom**: Usa Q/E para acercarte/alejarte
3. **Seguimiento**: Usa ratón para seguir partículas individuales
4. **Contraste**: Activa "Colores dinámicos" para ver velocidades

### ⚡ Para Mejor Rendimiento:
1. Reducir partículas a 100-150
2. Desactivar colisiones si no son necesarias
3. No activar estelas (consumen recursos)
4. Cerrar otras pestañas del navegador

### 🎮 Para Interacciones Divertidas:
1. **Modo FPS**: Navega entre las partículas
2. **Bombardeo**: Haz clicks rápidos para crear múltiples explosiones
3. **Persecución**: Intenta "atrapar" una partícula con la cámara

---

## 📝 Plantilla de Reporte de Experimento

Usa esta plantilla para documentar tus experimentos:

```markdown
## Experimento: [Nombre]

**Fecha**: [Tu fecha]
**Hipótesis**: [Qué esperas que pase]

### Configuración:
- Escenario base: [Cual]
- Gravedad: [Valor]
- Fricción: [Valor]
- Rebote: [Valor]
- Fuerza Central: [Valor]
- Otros: [Parámetros relevantes]

### Procedimiento:
1. [Paso 1]
2. [Paso 2]
3. [Paso 3]

### Observaciones:
[Qué observaste]

### Resultados:
[Qué pasó realmente]

### Conclusión:
[¿Se cumplió tu hipótesis? ¿Por qué sí o no?]

### Aprendizaje:
[Qué aprendiste sobre física]
```

---

## 🎓 Conexión con Conceptos del Curso

Este proyecto aplica:

### Diseño de Interfaces:
- ✅ Controles intuitivos y accesibles
- ✅ Feedback visual inmediato
- ✅ Jerarquía visual clara
- ✅ Diseño responsive

### Programación:
- ✅ POO (Clase Particula)
- ✅ Bucles de animación
- ✅ Gestión de eventos
- ✅ Optimización de rendimiento

### Computación Gráfica:
- ✅ Renderizado 3D
- ✅ Iluminación dinámica
- ✅ Sistemas de partículas
- ✅ Efectos visuales

### Matemáticas:
- ✅ Álgebra vectorial
- ✅ Trigonometría
- ✅ Integración numérica
- ✅ Geometría 3D

---

## ❓ Preguntas Frecuentes

**P: ¿Por qué las partículas atraviesan las paredes a veces?**  
R: Con velocidades muy altas, pueden "saltar" el límite entre frames. Aumenta la fricción o reduce las fuerzas.

**P: ¿Por qué se pone lento con muchas partículas?**  
R: La detección de colisiones es O(n²). Desactiva colisiones o reduce el número.

**P: ¿Cómo guardo mi configuración favorita?**  
R: Anota los valores. En futuras versiones se podría añadir export/import.

**P: ¿Puedo modificar el código?**  
R: ¡Claro! Abre simulacion-particulas.html con un editor y experimenta.

**P: ¿Qué navegador funciona mejor?**  
R: Chrome, Firefox y Edge modernos. Safari también funciona pero puede ser más lento.

---

## 🚀 Siguiente Nivel

Una vez domines los experimentos básicos:

1. **Modifica el código HTML**:
   - Cambia colores de las partículas
   - Añade más tipos de iluminación
   - Crea nuevas formas (cubos, conos)

2. **Añade nuevos escenarios**:
   - Copia la función `escenarioLluvia()`
   - Modifica los parámetros
   - Añade un botón nuevo

3. **Implementa nuevas fuerzas**:
   - Campo magnético
   - Turbulencia (ruido Perlin)
   - Atracción entre partículas cercanas

4. **Mejora las colisiones**:
   - Fusión de partículas-
   - Partículas que se dividen
   - Diferentes materiales

---

## 📚 Para Profundizar

Si te interesa seguir:

1. **Nature of Code** de Daniel Shiffman
2. **The Coding Train** (YouTube)
3. **Three.js Journey** (Curso completo)
4. **Game Physics Engine Development** de Ian Millington

---

**🎉 ¡Diviértete experimentando con la física!**

Recuerda: **La ciencia es probar, observar, preguntar y aprender.** No tengas miedo de romper cosas o conseguir resultados inesperados. ¡Eso es exactamente lo que hacen los verdaderos científicos!

---

*Última actualización: 8 de febrero de 2026*
