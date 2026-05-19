# Sistema de Gestión de Procesos Empresariales - Editor de Nodos

## 📋 Descripción

Sistema visual de gestión empresarial basado en nodos interconectados, diseñado para crear flujos de trabajo empresariales de forma intuitiva. A diferencia de los sistemas ERP tradicionales basados en formularios, este sistema utiliza un enfoque visual donde los procesos se representan mediante nodos que se pueden arrastrar y conectar entre sí.

## 🎯 Objetivo

Desarrollar un entorno visual para gestión empresarial que permita:
- Crear flujos de procesos de negocio arrastrando nodos
- Conectar diferentes etapas del proceso empresarial
- Ejecutar flujos completos de forma visual
- Gestionar órdenes de compra, clientes, productos y aprobaciones

## 🚀 Características

### Versión 1.0 (Básica)
- ✅ Editor de nodos drag & drop
- ✅ Conexiones entre nodos
- ✅ Nodos básicos de gestión empresarial:
  - Cliente
  - Producto
  - Orden de Compra
  - Aprobación
  - Registro
- ✅ Ejecución de flujos
- ✅ Consola de logs

### Futuras mejoras
- 🔄 Conexión con base de datos
- 🔄 Persistencia de flujos
- 🔄 Más tipos de nodos empresariales
- 🔄 Mejoras visuales y animaciones
- 🔄 Exportación/importación de flujos
- 🔄 Reportes y estadísticas

## 🛠️ Tecnologías

- **Backend**: Python + Flask
- **Frontend**: JavaScript Vanilla (ES6 Modules)
- **Estilos**: CSS3 con Grid y Flexbox
- **Arquitectura**: Modular y extensible

## 📦 Instalación

```bash
# Instalar dependencias
pip install flask

# Ejecutar servidor
python app.py

# Abrir en navegador
http://localhost:5000
```

## 📁 Estructura del Proyecto

```
301-002-101/
├── app.py                 # Servidor Flask principal
├── modules/               # Módulos backend (nodos)
│   ├── __init__.py
│   ├── cliente.py
│   ├── producto.py
│   ├── orden_compra.py
│   ├── aprobar.py
│   └── registro.py
├── static/                # Archivos estáticos
│   ├── app.js            # Lógica frontend
│   ├── styles.css        # Estilos
│   └── modules/          # Módulos frontend (UI específica)
└── templates/             # Plantillas HTML
    └── index.html        # Interfaz principal
```

## 🎨 Temática del Proyecto

**Sistema de Gestión de Órdenes de Compra/Venta**

Este sistema permite crear flujos visuales para gestionar el proceso completo de una orden de compra:

1. **Cliente** → Información del cliente
2. **Producto** → Selección de productos
3. **Orden de Compra** → Creación de la orden
4. **Aprobación** → Proceso de aprobación/rechazo
5. **Registro** → Almacenamiento final

Cada etapa es un nodo que se conecta visualmente, permitiendo ver el flujo completo del proceso empresarial.

## 📝 Autor

Proyecto desarrollado para la asignatura "Sistemas de Gestión Empresarial"
DAM 2 - Segundo Trimestre

## 📅 Versiones

- **v1.0** (18/02/2026): Versión inicial con funcionalidad básica
