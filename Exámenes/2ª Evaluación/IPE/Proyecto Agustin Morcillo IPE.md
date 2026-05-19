# Plan de Sostenibilidad, Digitalización e IPE
## The BloomRoom — Centro de Bienestar Integral

| | |
|---|---|
| **Alumno** | Agustín Morcillo Aguado |
| **Rol en la empresa** | Co-fundador y desarrollador |
| **Ciclo Formativo** | Desarrollo de Aplicaciones Multiplataforma (DAM) |
| **Módulo** | Sostenibilidad, Digitalización e Innovación en Procesos Empresariales (IPE) |

---

## PARTE I — Contexto y análisis estratégico

### 1. La empresa: The BloomRoom

The BloomRoom es un centro de bienestar integral fundado en Valencia que ofrece servicios de yoga, pilates, meditación, masajes terapéuticos, coaching nutricional y talleres de bienestar. Está orientado a personas que buscan mejorar su calidad de vida de forma holística, combinando el cuidado físico, mental y emocional.

El equipo está formado por 10 profesionales especializados en distintas disciplinas del bienestar. Agustín Morcillo es co-fundador de The BloomRoom y responsable del desarrollo tecnológico de la empresa, encargándose de diseñar e implementar la infraestructura digital necesaria para hacer crecer el negocio de forma eficiente y sostenible desde su fundación.

Desde el inicio, The BloomRoom ha apostado por un modelo de negocio responsable: materiales ecológicos, productos naturales certificados y un enfoque en el bienestar colectivo que va más allá del servicio individual. La digitalización forma parte de su ADN desde el primer momento, como palanca para escalar el impacto sin sacrificar la calidad ni los valores fundacionales.

---

### 2. Análisis de materialidad

Antes de plantear cualquier mejora, es necesario identificar dónde la empresa tiene mayor impacto ambiental, social y operativo:

| Área | Problema identificado | Prioridad |
|------|-----------------------|-----------|
| **Energía** | Consumo eléctrico continuo en salas, climatización, iluminación y equipamiento audiovisual | Alta |
| **Residuos** | Aceites esenciales, velas, envases de cosméticos y materiales de un solo uso sin gestión diferenciada | Alta |
| **Digitalización** | Reservas por WhatsApp o teléfono, cobros manuales, sin historial de cliente ni comunicación centralizada | Alta |
| **Datos** | Sin sistema centralizado: imposible personalizar la experiencia ni extraer métricas de valor | Media |
| **Proveedores** | Falta de criterios de sostenibilidad en la cadena de suministro de productos del centro | Media |

---

### 3. ODS vinculados al proyecto

De los 17 Objetivos de Desarrollo Sostenible de la Agenda 2030, los más relevantes para The BloomRoom son:

| ODS | Nombre | Aplicación en The BloomRoom |
|-----|--------|-----------------------------|
| **ODS 3** | Salud y bienestar | La actividad del centro mejora directamente la salud física y mental de la población. La digitalización permite una experiencia más personalizada y accesible. |
| **ODS 7** | Energía asequible y no contaminante | Reducción del consumo energético, iluminación LED y valoración de suministro eléctrico renovable. |
| **ODS 9** | Industria, innovación e infraestructura | Desarrollo de una app multiplataforma propia que moderniza la infraestructura digital del centro. |
| **ODS 12** | Producción y consumo responsable | Uso de productos naturales certificados, reducción de plásticos y gestión responsable de residuos. |
| **ODS 13** | Acción por el clima | Reducción de la huella de carbono mediante eficiencia energética y sesiones online que eliminan desplazamientos. |

---

## PARTE II — Plan de Digitalización

### 4. Diagnóstico digital: punto de partida

En el momento de lanzamiento de The BloomRoom, la gestión del centro se apoyaba en herramientas no integradas:

- Reservas gestionadas manualmente por WhatsApp o teléfono.
- Cobros en efectivo o por transferencia sin registro centralizado.
- Ausencia de historial por cliente.
- Comunicación interna entre profesionales sin ningún sistema estructurado.

Esta situación, habitual en negocios del sector wellness en sus primeras fases, genera problemas de escalabilidad, dificulta la fidelización de clientes y no permite extraer datos de valor para la toma de decisiones estratégicas.

---

### 5. Objetivo: la app multiplataforma de The BloomRoom

El objetivo es disponer de una aplicación multiplataforma desarrollada a medida, accesible desde móvil (iOS y Android) y navegador web, que centralice toda la operativa del centro en un único sistema:

- **Gestión de clientes:** perfil, historial de servicios, preferencias y comunicación personalizada.
- **Agenda y reservas:** reservas online en tiempo real, recordatorios automáticos y control de disponibilidad por instructor o sala.
- **Facturación y pagos:** generación de facturas digitales, gestión de bonos y packs, y seguimiento de cobros.
- **Inventario de productos:** control del stock de productos vendidos en recepción y materiales utilizados en tratamientos.
- **Panel de métricas (IPE):** visualización en tiempo real de los KPIs operativos y de sostenibilidad del centro.

---

### 6. Mi aportación como co-fundador y desarrollador

Como co-fundador de The BloomRoom y responsable técnico del proyecto, Agustín Morcillo está desarrollando esta aplicación utilizando tecnologías multiplataforma (Flutter para el frontend móvil y web, con backend en Node.js y base de datos PostgreSQL).

**Funcionalidades implementadas:**

- Registro centralizado de clientes con historial de visitas, servicios contratados y preferencias de bienestar.
- Módulo de agenda con reservas online accesibles desde el móvil del cliente o desde la web del centro.
- Generación automática de facturas y envío por correo electrónico, eliminando el papel en el proceso de cobro.
- Control de stock de productos con alertas automáticas de reposición.
- Dashboard de indicadores en tiempo real: tasa de ocupación de salas, ingresos por línea de servicio, clientes activos y consumo de recursos.
- Módulo de sesiones en streaming para yoga, pilates y meditación sin necesidad de presencia física.

La arquitectura de la app separa roles (cliente, instructor, administración y dirección), garantizando que cada usuario accede únicamente a la información relevante para su función.

---

### 7. Protección de datos en la app (RGPD / LOPD)

The BloomRoom trata datos personales de sus clientes (nombre, contacto, historial de servicios, preferencias de salud y bienestar). El cumplimiento del RGPD y la LOPD es tanto una obligación legal como un compromiso ético del centro.

**Medidas técnicas implementadas en la app:**

- Cifrado de datos en reposo y en tránsito (TLS 1.3).
- Sistema de roles granular: los instructores solo acceden al historial de los clientes asignados a sus sesiones.
- Registro de auditoría (log de accesos): cualquier consulta o modificación del perfil de un cliente queda registrada con fecha, hora y usuario.
- Consentimiento informado integrado en el proceso de alta, con almacenamiento digital del registro.
- Gestión automatizada de bajas: los clientes pueden solicitar la eliminación de sus datos y el sistema lo ejecuta de forma trazable.

**Medidas organizativas:**

- Registro de Actividades de Tratamiento (RAT) actualizado.
- Acuerdos de encargado de tratamiento con todos los proveedores externos que accedan a datos de clientes.
- Protocolo de notificación de brechas a la AEPD en un plazo máximo de 72 horas.

---

## PARTE III — Plan de Sostenibilidad

### 8. Medidas inmediatas

**Eficiencia energética**

- Configurar todos los equipos en modo ahorro de energía tras 10 minutos de inactividad.
- Instalar iluminación LED de bajo consumo en todas las salas y zonas comunes.
- Establecer un protocolo de apagado completo al finalizar la jornada, con un responsable designado.

> _Indicador: registro mensual del consumo eléctrico con objetivo de reducción del 15% en 12 meses._

**Gestión responsable de residuos**

- Separar los residuos generados por los tratamientos (aceites, cosméticos, envases) según la clasificación municipal: orgánico, plástico, vidrio, papel y residuos especiales.
- Priorizar envases reutilizables o recargables para los productos de tratamiento.
- Eliminar el papel en recepción: contratos, consentimientos y facturas gestionados digitalmente desde la app.

---

### 9. Medidas a medio plazo

**Sesiones online y reducción de desplazamientos**

El módulo de streaming de la app permite impartir clases de yoga, pilates y meditación sin necesidad de presencia física. Esto amplía el alcance del centro, reduce los desplazamientos de los clientes y permite captar usuarios fuera del área geográfica inmediata.

**Suministro eléctrico renovable**

Verificar si el contrato de suministro eléctrico actual es con una comercializadora de energías renovables. En caso contrario, valorar el cambio como medida de alto impacto y coste nulo o reducido.

**Selección sostenible de productos**

Establecer un protocolo de compra que priorice proveedores con productos naturales certificados: ecológicos, cruelty-free y con envases reciclados.

---

### 10. Medidas a largo plazo

**Cláusulas sostenibles con proveedores**

A medida que The BloomRoom formalice sus contratos con proveedores externos, incorporar cláusulas que exijan el cumplimiento de criterios ambientales básicos: uso de envases reciclables, reducción de plásticos de un solo uso y compromiso con la economía circular.

**Comunicación del compromiso sostenible**

Publicar en la web y en la app información actualizada sobre las iniciativas de sostenibilidad en marcha, reforzando la imagen de marca responsable y generando confianza entre los clientes y la comunidad.

---

## PARTE IV — Gobernanza y Responsabilidad Social

### 11. Criterios ASG

Los criterios **ASG (Ambiental, Social y de Gobernanza)** evalúan de forma integral el compromiso sostenible de The BloomRoom:

| Criterio | Aplicación en The BloomRoom |
|----------|-----------------------------|
| **Ambiental** | Ahorro energético, iluminación LED, productos ecológicos certificados, reducción de plásticos, suministro renovable y sesiones online que reducen desplazamientos. |
| **Social** | Servicios de bienestar accesibles y de calidad, modelo laboral justo y colaborativo, sesiones online para personas con movilidad reducida o fuera del área, sesiones abiertas comunitarias. |
| **Gobernanza** | Cumplimiento del RGPD y la LOPD, sistema de roles y auditoría en la app, transparencia en métricas para la dirección y política de compra sostenible con proveedores. |

---

### 12. Responsabilidad Social Corporativa (RSC)

The BloomRoom entiende el bienestar como un compromiso que va más allá del cliente individual e incluye al equipo, la comunidad y el entorno:

- **Bienestar del equipo:** condiciones laborales dignas, horarios flexibles, formación continua y un entorno de trabajo coherente con los valores del negocio.
- **Accesibilidad:** la app sigue las pautas WCAG 2.1 y las sesiones online amplían el alcance a personas con diversidad funcional o limitaciones de movilidad.
- **Impacto comunitario:** organización periódica de sesiones abiertas gratuitas o de bajo coste para democratizar el acceso al bienestar.
- **Sensibilización interna:** formación al equipo en sostenibilidad, protección de datos y digitalización para alinear las prácticas cotidianas con los valores fundacionales.

---

## PARTE V — Medición, seguimiento y hoja de ruta

### 13. Indicadores de Procesos Empresariales (IPE)

El dashboard desarrollado por Agustín Morcillo permite a la dirección de The BloomRoom monitorizar en tiempo real los siguientes indicadores clave, sin necesidad de informes manuales:

| Indicador | Descripción | Objetivo |
|-----------|-------------|----------|
| **Tasa de ocupación** | % de horas disponibles vs. reservadas por sala o instructor | > 80% |
| **Tiempo medio de gestión** | Minutos dedicados a tareas administrativas por reserva | < 3 min |
| **Índice de satisfacción** | Encuesta digital post-sesión (escala 1-10) | > 8,5 |
| **Tasa de digitalización** | % de reservas y cobros gestionados sin papel | 100% en 6 meses |
| **Consumo energético mensual** | kWh consumidos mensualmente en el centro | − 15% en 12 meses |
| **Incidencias de datos** | Número de brechas o accesos no autorizados | 0 |
| **Residuos reciclados** | % de residuos generados correctamente separados | > 90% |

---

### 14. Plan de acción: hoja de ruta

| Medida | Área | Plazo | Coste estimado | Responsable |
|--------|------|-------|----------------|-------------|
| App multiplataforma de gestión | Digitalización | Inmediato | Desarrollo interno | Agustín Morcillo |
| Consentimiento digital y roles (RGPD) | Digital / Legal | Inmediato | Sin coste adicional | Agustín Morcillo |
| Dashboard de indicadores (IPE) | Digital / Dirección | Inmediato | Incluido en la app | Agustín Morcillo |
| Iluminación LED en salas | Sostenibilidad | Inmediato | Bajo (< 500 €) | Fundadores |
| Política de ahorro energético | Sostenibilidad | Inmediato | Sin coste | Fundadores |
| Protocolo de reciclaje de residuos | Sostenibilidad / RSC | Inmediato | Sin coste | Todo el equipo |
| Módulo de sesiones online | Digital / Sostenibilidad | Medio plazo | Incluido en la app | Agustín Morcillo |
| Suministro eléctrico renovable | Sostenibilidad | Medio plazo | Sin sobrecoste | Fundadores |
| Protocolo de compra sostenible | Sostenibilidad | Largo plazo | Sin coste directo | Fundadores |
| Comunicación RSC en web y app | RSC / Digital | Largo plazo | Bajo | Agustín Morcillo |

---

## Conclusión

En The BloomRoom, digitalización, sostenibilidad e innovación en procesos empresariales no son tres conceptos separados, sino tres dimensiones de un mismo proyecto empresarial.

La aplicación multiplataforma desarrollada por Agustín Morcillo como co-fundador y responsable técnico es el eje central de este plan: una herramienta que elimina el papel, automatiza la gestión de reservas y cobros, garantiza el cumplimiento del RGPD, genera indicadores de eficiencia en tiempo real y mejora la experiencia del cliente. Todo ello con desarrollo propio, lo que convierte la tecnología en una ventaja competitiva real desde el primer día.

El compromiso de The BloomRoom con la sostenibilidad y la responsabilidad social no responde únicamente a obligaciones legales, sino a una visión de empresa moderna, coherente y orientada tanto al impacto positivo en sus clientes como en su entorno.

---

_Documento elaborado en el marco del módulo de Sostenibilidad, Digitalización e IPE · DAM · Curso 2025-2026_
