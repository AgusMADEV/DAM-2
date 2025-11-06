En este ejercicio he analizado los **recursos materiales, humanos y económicos** necesarios para desarrollar una aplicación de **clasificación automática de facturas para PYMEs valencianas**, utilizando técnicas de inteligencia artificial.  

A lo largo del desarrollo he querido destacar también cómo mis aficiones personales, como el **deporte** y los **videojuegos**, contribuyen positivamente al rendimiento del proyecto. Practicar deporte de forma regular me ayuda a mantener la concentración y reducir la fatiga mental durante las largas sesiones de programación. Por otro lado, los videojuegos fortalecen mi capacidad de resolución de problemas, pensamiento lógico y toma de decisiones, cualidades directamente aplicables al desarrollo de software.

---

### 🖥️ Recursos materiales  
He calculado las especificaciones necesarias tanto para el servidor de desarrollo como para el de producción.

| Tipo de servidor | CPU | RAM | Almacenamiento | Costo estimado |
|------------------|------|-----|----------------|----------------|
| **Desarrollo (local)** | 4 cores | 8 GB | 256 GB SSD | 600 € (equipo propio) |
| **Producción (nube)** | 8 cores | 16 GB | 512 GB SSD | 80 €/mes (Google Cloud VM) |

Se implementaría **RAID 1** para la redundancia de datos, ya que este sistema permite duplicar la información en dos discos, garantizando la seguridad de los documentos procesados.

### 👨‍💻 Recursos humanos  
Para ofrecer soporte técnico 24/7, se requieren tres técnicos distribuidos en turnos rotativos de 8 horas.

- **Salario neto por persona:** 1.200 €/mes  
- **Coste bruto (incluyendo Seguridad Social):** 1.650 €/mes  
- **Número de técnicos:** 3  
- **Coste mensual total:** 4.950 €  
- **Coste anual total:** 59.400 €  

Los técnicos deben tener conocimientos en administración de servidores, bases de datos y atención al cliente. Además, he estimado una **formación inicial de dos semanas** para familiarizarse con la aplicación y los protocolos internos.

### 💶 Recursos económicos  
El entrenamiento del modelo de IA y los servicios en la nube representan los principales costes adicionales.

| Concepto | Descripción | Costo estimado |
|-----------|--------------|----------------|
| Entrenamiento con GPU | 200 horas a 1,20 €/h | 240 € |
| APIs IA (OpenAI, Google) | Tokens mensuales (uso moderado) | 60 €/mes |
| Datasets etiquetados | Facturas reales y anotadas | 300 € |
| Licencias y dominios | Certificados SSL, dominio, software | 100 €/año |
| **Total estimado (primer año)** |  | **1.360 €** |

---

### 🔹 Ejemplo 1: Servidor mínimo necesario  
Para un entorno de pruebas y desarrollo capaz de procesar hasta 10 documentos simultáneamente:
- **CPU:** 4 cores  
- **RAM:** 8 GB  
- **Almacenamiento:** 256 GB SSD  
- **Costo estimado:** 40 €/mes (en un servidor cloud económico)  

Esto permite un rendimiento adecuado para desarrollo sin incurrir en gastos innecesarios.

### 🔹 Ejemplo 2: Presupuesto anual de personal  
El presupuesto anual para tres técnicos trabajando en turnos rotativos se calcula así:
```
1.650 € (coste bruto) x 3 técnicos x 12 meses = 59.400 €/año
```
Con esta estructura se asegura un soporte continuo, evitando caídas del servicio y manteniendo una atención constante al cliente.

---

Este análisis me ha permitido comprender cómo los recursos materiales, humanos y económicos influyen directamente en la **eficiencia y viabilidad** de un proyecto de desarrollo.  
Seleccionar correctamente el servidor, planificar el presupuesto y calcular los costes de personal son pasos esenciales para mantener el equilibrio entre calidad técnica y sostenibilidad económica.  

Además, integrar hábitos saludables como el **deporte** y actividades recreativas como los **videojuegos** en mi rutina de trabajo me ayuda a ser más productivo, mantener la motivación y mejorar mis habilidades cognitivas.  

En conclusión, esta práctica no solo me ha servido para afianzar los conocimientos de planificación y gestión de recursos, sino también para valorar la importancia del equilibrio personal en el proceso creativo y técnico.