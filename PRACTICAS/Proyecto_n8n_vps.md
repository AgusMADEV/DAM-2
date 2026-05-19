# Proyecto n8n en VPS

**Proyecto:** Instalación y puesta en marcha de n8n en VPS Linux (IONOS)  
**Servidor:** VPS Linux Ubuntu  
**Responsable(s):** Agustín / Equipo  
**Fecha de inicio:** 09 /03 / 2026  
**Última actualización:** 13 / 03 / 2026
**Estado general:** En curso

---

## 1. Objetivo del documento

Guía de trabajo y registro de avance para la instalación de **n8n** en un servidor **VPS Linux de IONOS**.

También recoge el análisis previo realizado sobre la viabilidad técnica, la arquitectura recomendada, las decisiones tomadas y el seguimiento paso a paso durante la instalación.

---

## 2. Análisis e investigación previa

### 2.1. Qué es n8n

n8n es una plataforma de automatización de flujos de trabajo (*workflows*) que permite conectar servicios, APIs, bases de datos y tareas internas mediante un editor visual.

### 2.2. ¿n8n necesita instalación?

Sí. n8n puede usarse de dos maneras:

- **n8n Cloud:** servicio gestionado por n8n, sin necesidad de instalar nada en un servidor propio.
- **n8n Self-Hosted:** instalación en infraestructura propia, por ejemplo un VPS Linux.

### 2.3. Conclusión sobre el VPS

Se ha confirmado que **sí es posible instalar n8n en un VPS Linux de IONOS**.  
La opción más adecuada para un entorno estable y mantenible es desplegarlo en modo **self-hosted** sobre Ubuntu, preferiblemente usando:

- Docker
- Docker Compose
- Proxy inverso (Caddy, Nginx o Traefik)
- HTTPS
- Base de datos PostgreSQL

### 2.4. Motivo de la arquitectura elegida

Se elige una instalación con Docker Compose porque:

- simplifica el despliegue
- facilita actualizaciones
- permite separar servicios
- mejora la portabilidad
- deja una estructura más limpia y documentable

Se elige PostgreSQL porque ofrece una base más sólida y escalable que SQLite para entornos reales o en crecimiento.

### 2.5. Punto importante sobre automatizaciones

Una vez instalado n8n en el servidor, las automatizaciones se crean y se gestionan **dentro de la propia instancia de n8n**, desde su interfaz web.

Es decir:

1. primero se instala n8n en el VPS,
2. después se accede a la interfaz,
3. y ahí se crean, prueban y activan los workflows.

---

## 3. Arquitectura prevista

### 3.1. Componentes principales

- **Servidor VPS Linux (IONOS)**
- **Ubuntu Server**
- **Docker**
- **Docker Compose**
- **n8n**
- **PostgreSQL**
- **Caddy** como proxy inverso y gestor de certificados SSL
- **Dominio o subdominio** apuntando al VPS

### 3.2. Esquema simplificado

```text
Usuario -> HTTPS -> Caddy -> n8n
                    |
                    -> PostgreSQL
```

---

## 4. Requisitos previos

Marcar según se vaya completando.

- [ X] Acceso SSH al VPS
- [ X] Usuario con permisos sudo
- [ X] Ubuntu actualizado
- [ ] Dominio o subdominio configurado
- [ ] DNS apuntando a la IP del VPS
- [ ] Puertos 80 y 443 abiertos
- [ X] Docker instalado
- [ X] Docker Compose disponible
- [ ] Firewall revisado
- [ ] Decidida la contraseña de PostgreSQL
- [ ] Definida la clave de cifrado de n8n (`N8N_ENCRYPTION_KEY`)
- [ ] Confirmada zona horaria (`Europe/Madrid`)

---

## 5. Plan de ejecución

### Fase 1. Preparación del servidor

- actualizar paquetes
- instalar dependencias básicas
- instalar Docker
- instalar Docker Compose plugin
- habilitar Docker al arranque
- revisar firewall

**Estado:** Completado

### Fase 2. Preparación de red y acceso

- configurar dominio/subdominio
- comprobar resolución DNS
- abrir puertos 80 y 443
- verificar acceso externo

**Estado:** En curso

### Fase 3. Preparación de estructura del proyecto

- crear directorios de trabajo
- crear archivo `.env`
- preparar `docker-compose.yml`
- preparar configuración del proxy inverso

**Estado:** Pendiente

### Fase 4. Despliegue de servicios

- levantar PostgreSQL
- levantar n8n
- levantar Caddy
- comprobar estado de contenedores
- validar emisión de certificado SSL

**Estado:** Pendiente

### Fase 5. Validación funcional

- acceder a la interfaz web
- crear usuario propietario inicial
- comprobar persistencia de datos
- validar webhooks
- validar configuración horaria
- documentar resultado final

**Estado:** Pendiente

---

## 6. Registro de pasos realizados

| Nº | Fecha | Paso realizado | Comando / acción | Resultado | Responsable | Estado |
|---|---|---|---|---|---|---|
| 1 | 09/03/2026 | Conexión inicial al VPS vía SSH | `ssh usuario@ip_vps` | Acceso establecido correctamente | Agustín | Completado |
| 2 | 09/03/2026 | Actualización del sistema Ubuntu | `sudo apt update && sudo apt upgrade -y` | Sistema actualizado sin errores | Agustín | Completado |
| 3 | 09/03/2026 | Instalación de Docker | Instalación oficial de Docker Engine | Docker instalado y operativo | Agustín | Completado |
| 4 | 09/03/2026 | Instalación de Docker Compose | `sudo apt install docker-compose-plugin` | Docker Compose disponible | Agustín | Completado |
| 5 | 10/03/2026 | Verificación de versiones | `docker --version` y `docker compose version` | Versiones confirmadas | Agustín | Completado |
| 6 | 12/03/2026 | Análisis de arquitectura y documentación | Investigación sobre n8n self-hosted | Arquitectura definida con PostgreSQL + Caddy | Agustín | Completado |
| 7 |  | Configuración de dominio/DNS | Apuntar DNS a IP del VPS | Pendiente de verificación | Agustín | En curso |
| 8 |  | Revisión y configuración de firewall | `sudo ufw status` y configuración de puertos 80/443 |  |  | Pendiente |
| 9 |  | Generación de N8N_ENCRYPTION_KEY | `openssl rand -hex 32` |  |  | Pendiente |
| 10 |  | Creación de estructura de directorios | `mkdir -p ~/n8n/{data,caddy_data,postgres_data}` |  |  | Pendiente |
| 11 |  | Creación de archivo .env | Definir todas las variables de entorno |  |  | Pendiente |
| 12 |  | Creación de docker-compose.yml | Configurar servicios n8n, PostgreSQL y Caddy |  |  | Pendiente |
| 13 |  | Levantamiento de servicios | `docker compose up -d` |  |  | Pendiente |
| 14 |  | Verificación de contenedores | `docker compose ps` |  |  | Pendiente |
| 15 |  | Acceso a interfaz web de n8n | Acceder vía navegador a https://dominio |  |  | Pendiente |
| 16 |  | Creación de usuario propietario | Registro del primer usuario administrador |  |  | Pendiente |
| 17 |  | Validación de persistencia de datos | Reiniciar contenedores y verificar datos |  |  | Pendiente |
| 18 |  | Prueba de webhook de prueba | Crear workflow simple con webhook |  |  | Pendiente |

---

## 7. Comandos de referencia

### 7.1. Actualización del sistema

```bash
sudo apt update && sudo apt upgrade -y
```

### 7.2. Instalación base de utilidades

```bash
sudo apt install -y ca-certificates curl gnupg ufw
```

### 7.3. Comprobación de Docker

```bash
docker --version
docker compose version
```

### 7.4. Levantar servicios

```bash
docker compose up -d
```

### 7.5. Ver estado de contenedores

```bash
docker compose ps
```

### 7.6. Ver logs

```bash
docker compose logs -f
```

### 7.7. Reiniciar servicios

```bash
docker compose restart
```

### 7.8. Parar servicios

```bash
docker compose down
```

### 7.9. Actualizar contenedores

```bash
docker compose pull
docker compose up -d
```

---

## 8. Configuración prevista

### 8.1. Variables clave

```env
DOMAIN_NAME=n8n.tudominio.com
POSTGRES_DB=n8n
POSTGRES_USER=n8n
POSTGRES_PASSWORD=********
N8N_ENCRYPTION_KEY=********
GENERIC_TIMEZONE=Europe/Madrid
```

### 8.2. Ajustes importantes

- `WEBHOOK_URL` debe apuntar al dominio público de n8n.
- `N8N_PROXY_HOPS=1` debe configurarse si n8n está detrás de proxy inverso.
- La zona horaria debe quedar definida para evitar errores en tareas programadas.

---

## 9. Incidencias y decisiones técnicas

| Fecha | Incidencia / decisión | Impacto | Solución / criterio adoptado | Estado |
|---|---|---|---|---|
|  |  |  |  | Abierta |
|  |  |  |  | Abierta |
|  |  |  |  | Abierta |
|  |  |  |  | Abierta |

---

## 10. Validaciones finales

Marcar cuando se verifique cada punto.

- [ ] n8n responde correctamente por HTTPS
- [ ] El dominio apunta al VPS correctamente
- [ ] Caddy genera el certificado SSL
- [ ] PostgreSQL queda operativo
- [ ] n8n guarda configuración y credenciales
- [ ] La interfaz web carga sin errores
- [ ] Se ha creado el usuario inicial
- [ ] Los workflows pueden guardarse
- [ ] Los webhooks funcionan correctamente
- [ ] La hora del sistema y de n8n es correcta
- [ ] El reinicio del VPS no rompe el despliegue

---

## 11. Automatizaciones previstas tras la instalación

Este apartado se puede usar una vez la plataforma esté operativa.

| Nº | Automatización | Objetivo | Estado | Notas |
|---|---|---|---|---|
| 1 |  |  | Pendiente |  |
| 2 |  |  | Pendiente |  |
| 3 |  |  | Pendiente |  |
| 4 |  |  | Pendiente |  |

---

## 12. Mantenimiento posterior

Tareas recomendadas después de la instalación:

- revisar logs periódicamente
- actualizar imagen de n8n y contenedores
- hacer copias de seguridad de datos y base de datos
- revisar certificados SSL
- documentar cambios de configuración
- registrar nuevas automatizaciones implementadas

---

## 13. Resumen ejecutivo

Se ha investigado la viabilidad de instalar n8n en un VPS Linux de IONOS y se ha confirmado que es totalmente posible en modo self-hosted.

La arquitectura elegida busca una instalación limpia, segura y mantenible, apoyada en Docker Compose, PostgreSQL y un proxy inverso con HTTPS.

Este documento servirá como guía de trabajo y bitácora para registrar el progreso real, las decisiones tomadas y el estado de la instalación en cada fase.

---

## 14. Observaciones

Anotar aquí cualquier detalle adicional que convenga conservar:

- Este documento se ha creado como guía preliminar y plantilla de seguimiento. Debe actualizarse conforme avance la instalación real.
- La `N8N_ENCRYPTION_KEY` debe generarse de forma segura (32+ caracteres aleatorios) y guardarse en lugar seguro, ya que será necesaria para descifrar credenciales almacenadas.
- Es crítico que el dominio/subdominio esté correctamente configurado y resolviendo a la IP del VPS **antes** de iniciar Caddy, para evitar problemas con la emisión del certificado SSL de Let's Encrypt.
- Se recomienda realizar un backup del archivo `.env` con todas las credenciales en ubicación segura fuera del servidor.
- Verificar que el firewall del VPS (UFW o iptables) tiene los puertos 80 y 443 abiertos. Algunos proveedores también tienen firewall a nivel de panel de control.
- Considerar preparar un plan de rollback: documentar estado inicial del servidor y tener copias de seguridad antes de cambios mayores.
- El volumen de PostgreSQL debe persistirse correctamente en `docker-compose.yml` para evitar pérdida de datos ante reinicios.
- Recordar completar la tabla de **Registro de pasos realizados** (sección 6) conforme se ejecute cada comando, incluyendo fecha, resultado y responsable.
- Una vez operativo, establecer recordatorios para mantenimiento: actualizaciones mensuales, revisión de logs, y backups semanales de la base de datos. 

