# Determinación de Recursos Necesarios para un Proyecto de Desarrollo

## Introducción

Como estudiantes de desarrollo de aplicaciones informáticas, es fundamental aprender a identificar y calcular correctamente todos los recursos necesarios para llevar a cabo un proyecto. Esta habilidad nos permitirá crear presupuestos realistas y planificar adecuadamente nuestros futuros emprendimientos tecnológicos.

En este ejercicio analizaremos los recursos materiales, humanos y económicos necesarios para desarrollar una aplicación informática, considerando tanto la fase de desarrollo como la de implantación y mantenimiento.

## Contexto del Proyecto

Imaginemos que vamos a desarrollar una aplicación de clasificación automática de facturas para PYMEs valencianas (basándose en nuestros análisis previos de necesidades del mercado). Esta aplicación utilizará inteligencia artificial para automatizar el procesamiento de documentos y ayudar a las pequeñas empresas a reducir tareas administrativas repetitivas.

Durante el desarrollo intensivo del proyecto, es importante mantener un equilibrio vida-trabajo. Los deportes nos mantienen físicamente activos y mentalmente alertas, lo cual es crucial para rendir al máximo durante las largas sesiones de programación. Además, los videojuegos pueden ayudarnos en la resolución de problemas complejos y la toma de decisiones estratégicas, habilidades transferibles al desarrollo de software.

## Ejercicio: Análisis de Recursos

### Parte 1: Recursos Materiales

**Objetivo**: Determinar los componentes necesarios para el servidor mínimo que pueda ejecutar nuestro sistema de clasificación de facturas.

**Tareas a realizar**:

1. **Especificaciones del servidor de desarrollo**:
   - Investiga los requerimientos mínimos de hardware para ejecutar:
     - Python con librerías de IA (scikit-learn, TensorFlow)
     - Base de datos SQLite/PostgreSQL
     - Servidor web Flask
     - Procesamiento OCR (Tesseract)
   
2. **Configuración del servidor de producción**:
   - Determina las especificaciones necesarias considerando:
     - Procesador: ¿Cuántos cores necesitamos?
     - Memoria RAM: ¿Cuánta memoria para procesar múltiples documentos simultáneamente?
     - Almacenamiento SSD: ¿Qué capacidad para almacenar documentos y bases de datos?
     - Software RAID 1: ¿Por qué es importante para la redundancia de datos?

3. **Cálculo de costes**:
   - Investiga precios de componentes para montar el servidor
   - Compara con opciones de alquiler en la nube (AWS, Azure, Google Cloud)
   - Calcula costes de licencias de software necesario

**Entregable**: Tabla comparativa con especificaciones técnicas y costes (compra vs alquiler)

### Parte 2: Recursos Humanos

**Objetivo**: Establecer la necesidad de soporte técnico 24/7 para nuestra aplicación.

**Escenario**: Nuestra aplicación de clasificación de facturas será utilizada por PYMEs que operan en diferentes horarios. Necesitamos garantizar disponibilidad continua del servicio.

**Tareas a realizar**:

1. **Análisis de turnos**:
   - Calcula la distribución de turnos para cobertura 24 horas
   - Considera: 3 turnos de 8 horas cada uno
   - Incluye rotaciones de fines de semana y festivos

2. **Cálculo presupuestario**:
   - Salario neto propuesto por persona: 1.200€/mes
   - Calcula el coste bruto para la empresa (incluye Seguridad Social)
   - Multiplica por 3 personas para los diferentes turnos
   - Proyecta el presupuesto anual total

3. **Análisis de perfiles necesarios**:
   - ¿Qué conocimientos técnicos debe tener el personal de soporte?
   - ¿Necesitan formación específica en nuestro sistema?
   - ¿Cuánto tiempo de formación inicial estimamos?

**Entregable**: Presupuesto detallado de recursos humanos con justificación de los costes

### Parte 3: Recursos Económicos

**Objetivo**: Analizar los costes asociados con el entrenamiento y fine-tuning del sistema de IA.

**Contexto**: Nuestro sistema necesita ser entrenado con datos reales de facturas para mejorar su precisión en la clasificación automática.

**Tareas a realizar**:

1. **Costes de entrenamiento de IA**:
   - Investiga el coste por hora de uso de GPUs para entrenar modelos
   - Estima cuántas horas de entrenamiento necesitaremos
   - Calcula el coste de tokens si usamos APIs de modelos preentrenados (OpenAI, Google, etc.)

2. **Recursos de datos**:
   - ¿Cuánto cuesta obtener datasets de facturas etiquetadas?
   - ¿Necesitamos contratar servicios de etiquetado de datos?
   - ¿Qué costes legales implica el tratamiento de datos (GDPR)?

3. **Herramientas y servicios**:
   - Licencias de herramientas de desarrollo
   - Servicios en la nube para almacenamiento
   - Costes de certificaciones SSL, dominio, etc.