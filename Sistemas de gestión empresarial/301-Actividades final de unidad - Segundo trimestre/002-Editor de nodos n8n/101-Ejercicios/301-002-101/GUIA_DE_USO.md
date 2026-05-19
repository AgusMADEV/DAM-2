# Guía de Uso - Sistema de Gestión Empresarial

## 🚀 Cómo Ejecutar

1. **Abrir terminal** en la carpeta del proyecto
2. **Ejecutar** el servidor:
   ```bash
   python app.py
   ```
3. **Abrir navegador** automáticamente en `http://localhost:5000`

## 📖 Cómo Usar

### Crear un Flujo Básico

1. **Arrastra nodos** desde el panel izquierdo al lienzo central
2. **Configura** cada nodo haciendo clic en él y editando sus campos
3. **Conecta nodos** arrastrando desde el puerto de salida (●) hacia el puerto de entrada (●)
4. **Ejecuta** el flujo con el botón "▶ Ejecutar Flujo"
5. **Observa** los resultados en la consola derecha

### Ejemplo de Flujo: Orden de Compra

```
[Cliente] ──┐
            ├──> [Orden de Compra] ──> [Aprobar] ──> [Registro]
[Producto] ─┘
```

**Paso a paso:**

1. Arrastra nodo **👤 Cliente** y completa:
   - Nombre: "Juan Pérez"
   - Email: "juan@empresa.com"
   - Teléfono: "123456789"

2. Arrastra nodo **📦 Producto** y completa:
   - Nombre: "Laptop HP"
   - Precio: 899
   - Cantidad: 2

3. Arrastra nodo **📝 Orden de Compra** y completa:
   - Número de Orden: "ORD-2026-001"

4. Arrastra nodo **✅ Aprobar** y completa:
   - Monto Máximo: 2000

5. Arrastra nodo **💾 Registro**

6. **Conecta** los nodos en orden:
   - Cliente → Orden de Compra
   - Producto → Orden de Compra
   - Orden de Compra → Aprobar
   - Aprobar → Registro

7. **Ejecuta** con el botón ▶

### Controles

- **Zoom**: Ctrl + Rueda del ratón
- **Pan**: Ctrl + Arrastrar con ratón
- **Seleccionar nodo**: Click sobre el nodo
- **Eliminar nodo**: Seleccionar + Supr (o botón 🗑)
- **Conectar**: Arrastrar desde ● salida a ● entrada

## 🎓 Conceptos Clave

### Tipos de Nodos

1. **👤 Cliente**: Datos del cliente (nombre, email, teléfono)
2. **📦 Producto**: Información del producto con cálculo de total
3. **📝 Orden de Compra**: Combina clientes y productos en una orden
4. **✅ Aprobar**: Valida la orden según criterios (ej: monto máximo)
5. **💾 Registro**: Guarda/muestra el resultado final

### Flujo de Datos

- Los datos fluyen de **izquierda a derecha**
- Cada nodo recibe datos de sus **entradas** (inputs)
- Procesa la información según su **configuración**
- Devuelve un **resultado** que pasa al siguiente nodo

### Ejecución

- El sistema ejecuta los nodos en **orden topológico**
- Comienza por los nodos **sin entradas**
- Procesa según las **conexiones** establecidas
- Los resultados se muestran en la **consola**

## 🛠️ Mejoras Futuras Sugeridas

### Funcionales

1. **Persistencia**
   - Guardar flujos en localStorage/base de datos
   - Cargar flujos guardados
   - Exportar/importar JSON

2. **Más Nodos Empresariales**
   - Inventario
   - Facturación
   - Envío/Logística
   - Notificaciones (email, SMS)
   - Descuentos/Promociones
   - Reportes

3. **Base de Datos**
   - Conectar con SQLite/MySQL
   - CRUD de clientes/productos reales
   - Historial de órdenes

4. **Validaciones**
   - Validar campos obligatorios
   - Verificar ciclos en el grafo
   - Mensajes de error más descriptivos

5. **Condicionales y Bucles**
   - Nodos IF/ELSE
   - Bucles FOR/WHILE
   - Switch/Case

### Visuales

1. **Animaciones**
   - Animación del flujo de datos
   - Highlight de nodos activos
   - Transiciones suaves

2. **Temas**
   - Modo oscuro/claro
   - Personalización de colores
   - Diferentes estilos de nodos

3. **Iconografía**
   - Iconos SVG para cada tipo de nodo
   - Indicadores de estado
   - Badges/notificaciones

4. **Grid Inteligente**
   - Snap to grid
   - Alineación automática
   - Minimap

5. **UX Mejorada**
   - Drag & drop de herramientas
   - Doble click para editar
   - Atajos de teclado
   - Tooltips mejorados

### Arquitectura

1. **Modularización**
   - Separar lógica de nodos en clases
   - Sistema de plugins
   - API REST completa

2. **Testing**
   - Tests unitarios para módulos
   - Tests de integración
   - Tests E2E

3. **Performance**
   - Virtualización para muchos nodos
   - Lazy loading de módulos
   - Optimización de renders

## 📚 Estructura de un Módulo

Para crear un nuevo tipo de nodo, crea un archivo en `modules/`:

```python
# modules/mi_nodo.py

TOOL = {
    "type": "mi_nodo",
    "label": "🎯 Mi Nodo",
    "description": "Descripción de lo que hace",
    "config": {
        "campo1": {
            "type": "string",      # string, number, boolean
            "label": "Etiqueta",
            "default": "valor"
        }
    }
}

def execute(config, context):
    """
    config: diccionario con la configuración del nodo
    context: {inputs: [...], node_id: "..."}
    
    Returns: {message: "...", value: ...}
    """
    valor = config.get("campo1", "")
    inputs = context.get("inputs", [])
    
    # Tu lógica aquí
    
    return {
        "message": "Mensaje para la consola",
        "value": {"resultado": "datos"}
    }
```

El sistema cargará automáticamente el módulo al iniciar.

## 🎯 Criterios de Evaluación

Recuerda que la evaluación se basa en:

1. **Modificaciones Visuales/Estéticas** (30%)
   - Diseño atractivo y profesional
   - Experiencia de usuario fluida
   - Uso de animaciones y transiciones
   - Responsive design

2. **Modificaciones Funcionales** (70%)
   - Nuevos tipos de nodos
   - Funcionalidades avanzadas
   - Conexión con bases de datos
   - Lógica de negocio compleja
   - Validaciones y manejo de errores
   - Optimizaciones de código

## 💡 Ideas de Proyectos

Puedes adaptar este sistema para diferentes dominios:

- **Gestión de Restaurante**: Reservas → Mesa → Pedido → Cocina → Servicio
- **E-commerce**: Catálogo → Carrito → Pago → Envío → Entrega
- **Recursos Humanos**: Vacante → Candidato → Entrevista → Contratación
- **Logística**: Almacén → Picking → Empaquetado → Envío → Tracking
- **Proyectos**: Tarea → Asignación → Desarrollo → Revisión → Completado

## 📞 Soporte

Para dudas o problemas:
1. Revisar la consola del navegador (F12)
2. Verificar logs del servidor Python
3. Consultar README.md principal

¡Buena suerte con tu proyecto! 🚀
