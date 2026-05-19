# 📚 Índice del Proyecto

## 🏢 Sistema de Gestión de Procesos Empresariales - Editor de Nodos

**Versión**: 1.0  
**Fecha**: 18/02/2026  
**Autor**: DAM 2 - Sistemas de Gestión Empresarial  

---

## 📖 Documentación

### 1. [README.md](README.md) - Introducción al Proyecto
- 📋 Descripción general
- 🎯 Objetivos
- 🚀 Características
- 🛠️ Tecnologías utilizadas
- 📦 Instalación
- 📁 Estructura del proyecto

**Empieza por aquí** si es tu primera vez.

---

### 2. [GUIA_DE_USO.md](GUIA_DE_USO.md) - Manual de Usuario
- 🚀 Cómo ejecutar la aplicación
- 📖 Cómo usar el editor
- 🎓 Conceptos clave
- 💡 Ejemplos prácticos (flujo de orden de compra)
- 🛠️ Ideas de mejoras
- 📚 Cómo crear nuevos módulos

**Lee esto** para aprender a usar el sistema.

---

### 3. [ARQUITECTURA.md](ARQUITECTURA.md) - Diseño Técnico
- 📐 Diagramas de componentes
- 🔄 Flujos de ejecución
- 📦 Estructura de datos
- 🎨 Patrones de diseño utilizados
- 🔐 Seguridad y validación
- ⚡ Consideraciones de performance
- 🧪 Testing
- 📚 Extensibilidad

**Consulta esto** para entender cómo funciona internamente.

---

### 4. [IDEAS_MEJORAS.md](IDEAS_MEJORAS.md) - Roadmap de Desarrollo
- 🎨 Mejoras visuales y estéticas (30% nota)
- 🔧 Mejoras funcionales (70% nota)
- 🎯 Priorización de mejoras
- 📋 Checklist de implementación
- 💡 Consejos de desarrollo

**Usa esto** para planificar tus mejoras y obtener mejor nota.

---

### 5. [ESTADO_PROYECTO.md](ESTADO_PROYECTO.md) - Estado Actual
- ✅ Qué está implementado
- 🔄 Qué falta por hacer
- 🎯 Distribución del tiempo
- 📝 Notas de desarrollo
- 🧪 Testing checklist
- 📊 Objetivos de evaluación
- 🚀 Plan de acción recomendado

**Revisa esto** para saber en qué punto estás y qué hacer después.

---

## 🗂️ Estructura de Archivos

```
301-002-101/
│
├── 📄 INDEX.md              ← Estás aquí
├── 📄 README.md             ← Introducción
├── 📄 GUIA_DE_USO.md        ← Manual de usuario
├── 📄 ARQUITECTURA.md       ← Diseño técnico
├── 📄 IDEAS_MEJORAS.md      ← Roadmap
├── 📄 ESTADO_PROYECTO.md    ← Estado actual
│
├── 🐍 app.py                ← Servidor Flask
│
├── 📁 modules/              ← Módulos backend
│   ├── __init__.py          ← Cargador de módulos
│   ├── cliente.py           ← Nodo Cliente
│   ├── producto.py          ← Nodo Producto
│   ├── orden_compra.py      ← Nodo Orden
│   ├── aprobar.py           ← Nodo Aprobar
│   └── registro.py          ← Nodo Registro
│
├── 📁 static/               ← Archivos estáticos
│   ├── app.js               ← Lógica frontend
│   ├── styles.css           ← Estilos
│   └── 📁 modules/          ← Módulos frontend (vacío por ahora)
│
└── 📁 templates/            ← Plantillas HTML
    └── index.html           ← Interfaz principal
```

---

## 🚀 Inicio Rápido

### Ejecutar el Proyecto

```bash
# 1. Navegar a la carpeta
cd "d:\xampp\htdocs\DAM-2\Sistemas de gestión empresarial\301-Actividades final de unidad - Segundo trimestre\002-Editor de nodos n8n\101-Ejercicios\301-002-101"

# 2. Instalar dependencias (si es necesario)
pip install flask

# 3. Ejecutar servidor
python app.py

# 4. Abrir navegador en http://localhost:5000
```

### Crear tu Primer Flujo

1. Arrastra **👤 Cliente** al lienzo
2. Arrastra **📦 Producto** al lienzo
3. Arrastra **📝 Orden de Compra** al lienzo
4. Conecta Cliente → Orden de Compra
5. Conecta Producto → Orden de Compra
6. Haz clic en **▶ Ejecutar Flujo**
7. Observa los resultados en la consola

---

## 🎯 Objetivos del Proyecto

Este proyecto es la **actividad final de evaluación** del módulo de **Sistemas de Gestión Empresarial**.

### Conceptos Aprendidos

- ✅ Diseño de sistemas ERP visuales
- ✅ Arquitectura modular y extensible
- ✅ Comunicación cliente-servidor (API REST)
- ✅ Manipulación del DOM
- ✅ Grafos y algoritmos (BFS)
- ✅ Sistemas de plugins
- ✅ UX/UI para aplicaciones empresariales

### Criterios de Evaluación

- **30%**: Modificaciones estéticas y visuales
- **70%**: Modificaciones funcionales y código

**Objetivo**: Demostrar dominio avanzado de sistemas de gestión empresarial mediante un enfoque visual e innovador.

---

## 📞 Soporte y Recursos

### Problemas Comunes

**El servidor no inicia**
```bash
# Verificar Python instalado
python --version

# Verificar Flask instalado
pip list | grep -i flask

# Reinstalar Flask
pip install --upgrade flask
```

**Los nodos no se conectan**
- Asegúrate de arrastrar desde el puerto de **salida** (●) a la derecha
- Hacia el puerto de **entrada** (●) a la izquierda

**La ejecución no funciona**
- Verifica la consola del navegador (F12) para errores
- Revisa los logs del servidor Python en la terminal

### Debugging

**Frontend** (navegador):
```javascript
// En consola del navegador
console.log(nodos);        // Ver todos los nodos
console.log(conexiones);   // Ver todas las conexiones
console.log(TOOLS);        // Ver herramientas cargadas
```

**Backend** (servidor):
```python
# En app.py, añadir prints
print(f"Nodos recibidos: {nodes}")
print(f"Conexiones recibidas: {edges}")
```

---

## 📈 Próximos Pasos

### Para Principiantes
1. ✅ Ejecuta el proyecto y familiarízate
2. ✅ Crea flujos simples
3. ✅ Lee la documentación completa
4. 🔄 Modifica estilos CSS básicos
5. 🔄 Crea un nuevo tipo de nodo simple

### Para Nivel Intermedio
1. ✅ Todo lo anterior +
2. 🔄 Implementa base de datos SQLite
3. 🔄 Sistema de guardar/cargar flujos
4. 🔄 Añade 3-4 nodos empresariales nuevos
5. 🔄 Mejoras visuales (modo oscuro, animaciones)

### Para Nivel Avanzado
1. ✅ Todo lo anterior +
2. 🔄 Nodos condicionales con múltiples salidas
3. 🔄 Sistema de reportes y estadísticas
4. 🔄 Notificaciones reales (email/SMS)
5. 🔄 Undo/Redo
6. 🔄 Minimap
7. 🔄 Sistema de plugins completo

---

## 🌟 Características Destacadas

### Lo que hace especial a este proyecto

1. **Enfoque Visual Innovador**
   - No es el típico ERP con formularios
   - Flujos de trabajo visuales e intuitivos
   - Drag & drop fluido

2. **Arquitectura Extensible**
   - Sistema de plugins fácil de extender
   - Añadir nuevos nodos sin modificar core
   - Separación clara frontend/backend

3. **Código Limpio y Documentado**
   - Comentarios exhaustivos
   - Documentación completa
   - Patrones de diseño claros

4. **Base Sólida para Crecer**
   - Sistema básico funcional
   - Muchas posibilidades de mejora
   - Roadmap claro

---

## 🏆 Logros del Proyecto

- ✅ Sistema completamente funcional
- ✅ 5 tipos de nodos empresariales
- ✅ Ejecución de grafos complejos
- ✅ Interfaz moderna y profesional
- ✅ Documentación exhaustiva (>500 líneas)
- ✅ Código modular y mantenible
- ✅ Sin dependencias JS externas (vanilla)
- ✅ Responsive básico

---

## 📅 Historial de Versiones

### v1.0 - 18/02/2026 (Actual)
- Primera versión funcional
- Sistema básico de nodos
- 5 tipos de nodos empresariales
- Documentación completa

### v2.0 - Planificada (Futuro)
- Base de datos integrada
- Persistencia de flujos
- Nodos condicionales
- Mejoras visuales avanzadas

---

## 🎓 Recursos de Aprendizaje

### Tecnologías Utilizadas

**Backend**:
- [Flask Documentation](https://flask.palletsprojects.com/)
- [Python Type Hints](https://docs.python.org/3/library/typing.html)

**Frontend**:
- [MDN Web Docs - JavaScript](https://developer.mozilla.org/es/docs/Web/JavaScript)
- [MDN Web Docs - CSS Grid](https://developer.mozilla.org/es/docs/Web/CSS/CSS_Grid_Layout)
- [SVG Paths](https://developer.mozilla.org/es/docs/Web/SVG/Tutorial/Paths)

**Conceptos**:
- [Graph Theory - BFS](https://es.wikipedia.org/wiki/B%C3%BAsqueda_en_anchura)
- [Plugin Architecture](https://en.wikipedia.org/wiki/Plug-in_(computing))
- [REST API Design](https://restfulapi.net/)

---

## ✨ Agradecimientos

Este proyecto se basa en el trabajo realizado en clase durante el curso de **Sistemas de Gestión Empresarial**, módulo de **DAM 2**.

Inspirado en herramientas como:
- n8n (automatización de workflows)
- Node-RED (programación visual)
- Apache NiFi (flujos de datos)

---

## 📜 Licencia

Este proyecto es educativo y forma parte de las actividades del curso.  
Puedes usar, modificar y compartir el código libremente.

---

**¡Éxito con tu proyecto!** 🚀

---

*Última actualización: 18/02/2026*
