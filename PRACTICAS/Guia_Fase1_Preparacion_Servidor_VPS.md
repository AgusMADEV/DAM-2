# Guía Fase 1: Preparación del Servidor VPS IONOS Linux

**Proyecto:** Instalación de n8n en VPS  
**Fase:** 1 - Preparación del servidor  
**Sistema:** Ubuntu Server (IONOS VPS)  
**Fecha:** 16/03/2026

---

## Índice

1. [Requisitos previos](#requisitos-previos)
2. [Paso 1: Conexión al servidor](#paso-1-conexión-al-servidor)
3. [Paso 2: Actualización de paquetes](#paso-2-actualización-de-paquetes)
4. [Paso 3: Instalación de dependencias básicas](#paso-3-instalación-de-dependencias-básicas)
5. [Paso 4: Instalación de Docker](#paso-4-instalación-de-docker)
6. [Paso 5: Instalación de Docker Compose](#paso-5-instalación-de-docker-compose)
7. [Paso 6: Habilitar Docker al arranque](#paso-6-habilitar-docker-al-arranque)
8. [Paso 7: Revisar y configurar firewall](#paso-7-revisar-y-configurar-firewall)
9. [Verificación final](#verificación-final)
10. [Troubleshooting](#troubleshooting)

---

## Requisitos previos

Antes de comenzar, asegúrate de tener:

- ✅ IP pública del VPS de IONOS
- ✅ Usuario con acceso SSH (root o usuario con sudo)
- ✅ Contraseña o clave SSH para acceder
- ✅ Cliente SSH instalado en tu equipo local (PuTTY, Windows Terminal, etc.)

---

## Paso 1: Conexión al servidor

### 1.1. Desde Windows (PowerShell o CMD)

```bash
ssh root@TU_IP_VPS
```

O si usas un usuario no root:

```bash
ssh tu_usuario@TU_IP_VPS
```

### 1.2. Primera conexión

Si es la primera vez que te conectas, verás un mensaje preguntando si confías en el servidor:

```
The authenticity of host 'xxx.xxx.xxx.xxx' can't be established.
Are you sure you want to continue connecting (yes/no)?
```

Escribe `yes` y presiona Enter.

### 1.3. Verificar acceso

Una vez dentro, verifica que estás en el servidor correcto:

```bash
hostname
```

```bash
whoami
```

---

## Paso 2: Actualización de paquetes

### 2.1. Actualizar lista de paquetes

```bash
sudo apt update
```

**Resultado esperado:** Listado de paquetes disponibles para actualizar.

### 2.2. Actualizar todos los paquetes instalados

```bash
sudo apt upgrade -y
```

**Nota:** El parámetro `-y` confirma automáticamente las instalaciones.

**Tiempo estimado:** 2-5 minutos (depende de cuántas actualizaciones haya).

### 2.3. Limpiar paquetes antiguos (opcional pero recomendado)

```bash
sudo apt autoremove -y
```

### 2.4. Verificar versión del sistema

```bash
lsb_release -a
```

**Resultado esperado:** Información de Ubuntu (versión 20.04, 22.04 o superior).

---

## Paso 3: Instalación de dependencias básicas

### 3.1. Instalar paquetes esenciales

```bash
sudo apt install -y ca-certificates curl gnupg lsb-release
```

**Descripción de paquetes:**
- `ca-certificates`: Certificados de autoridades certificadoras
- `curl`: Herramienta para transferir datos
- `gnupg`: Herramientas de encriptación y firma
- `lsb-release`: Información sobre la distribución de Linux

### 3.2. Verificar instalación

```bash
curl --version
```

---

## Paso 4: Instalación de Docker

### 4.1. Eliminar versiones antiguas de Docker (si existen)

```bash
sudo apt remove docker docker-engine docker.io containerd runc
```

**Nota:** No pasa nada si muestra que no están instalados.

### 4.2. Añadir repositorio oficial de Docker

#### 4.2.1. Crear directorio para claves GPG

```bash
sudo install -m 0755 -d /etc/apt/keyrings
```

#### 4.2.2. Descargar clave GPG de Docker

```bash
curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo gpg --dearmor -o /etc/apt/keyrings/docker.gpg
```

#### 4.2.3. Dar permisos de lectura a la clave

```bash
sudo chmod a+r /etc/apt/keyrings/docker.gpg
```

#### 4.2.4. Añadir repositorio de Docker

```bash
echo \
  "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu \
  $(lsb_release -cs) stable" | sudo tee /etc/apt/sources.list.d/docker.list > /dev/null
```

**Explicación detallada del comando:**

Este comando largo es en realidad muy lógico si lo desglosamos por partes:

**1. `echo \`** → Imprime un texto. La barra invertida `\` permite continuar el comando en varias líneas.

**2. `"deb [arch=$(dpkg --print-architecture) ...]"`** → El texto que se va a escribir. Analicémoslo:

- **`deb`** → Indica que es un repositorio de paquetes Debian/Ubuntu
- **`arch=$(dpkg --print-architecture)`** → Detecta automáticamente la arquitectura de tu sistema
  - En la mayoría de casos será `amd64` (64 bits)
  - El símbolo `$(...)` ejecuta el comando y usa su resultado
- **`signed-by=/etc/apt/keyrings/docker.gpg`** → Indica qué clave GPG usar para verificar la autenticidad de los paquetes (la que descargamos en el paso anterior)
- **`https://download.docker.com/linux/ubuntu`** → URL del repositorio oficial de Docker para Ubuntu
- **`$(lsb_release -cs)`** → Detecta automáticamente tu versión de Ubuntu
  - Por ejemplo: `focal` (20.04), `jammy` (22.04), `noble` (24.04)
  - El símbolo `$(...)` ejecuta el comando y usa su resultado
- **`stable`** → Indica que queremos la versión estable de Docker (no beta ni testing)

**3. `| sudo tee /etc/apt/sources.list.d/docker.list`** → Guarda el texto en un archivo

- **`|`** → Envía la salida del comando anterior al siguiente
- **`sudo tee`** → Escribe el contenido en un archivo con permisos de superusuario
- **`/etc/apt/sources.list.d/docker.list`** → Ruta donde se crea el archivo de configuración del repositorio

**4. `> /dev/null`** → Oculta la salida en pantalla (hace el comando más limpio)

**Ejemplo práctico:**

Si tu sistema es Ubuntu 22.04 con arquitectura de 64 bits, el comando generaría internamente algo como:

```
deb [arch=amd64 signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/ubuntu jammy stable
```

Y ese texto se guardaría en el archivo `/etc/apt/sources.list.d/docker.list`.

**¿Por qué es importante?**

Este paso le dice a Ubuntu: "A partir de ahora, cuando busques paquetes para instalar, también busca en el repositorio oficial de Docker, y verifica su autenticidad con la clave GPG que descargamos".

Sin este paso, cuando intentes instalar Docker con `apt install`, Ubuntu no sabría dónde buscar los paquetes oficiales de Docker.

### 4.3. Actualizar lista de paquetes con el nuevo repositorio

```bash
sudo apt update
```

### 4.4. Instalar Docker Engine

```bash
sudo apt install -y docker-ce docker-ce-cli containerd.io docker-buildx-plugincleart
```

**⚠️ IMPORTANTE:** Este comando puedes ejecutarlo desde **cualquier directorio** del servidor. Los comandos `apt install` instalan software a nivel del sistema operativo, no en una carpeta específica.

**Tiempo estimado:** 2-3 minutos.

**¿Qué se está instalando?**

- **`docker-ce`** → Docker Community Edition (el motor principal de Docker)
- **`docker-ce-cli`** → CLI (interfaz de línea de comandos) para interactuar con Docker
- **`containerd.io`** → Runtime de bajo nivel que gestiona los contenedores
- **`docker-buildx-plugin`** → Plugin para construcción avanzada de imágenes Docker

**Parámetro `-y`:** Confirma automáticamente todas las preguntas de instalación.

### 4.5. Verificar que Docker está instalado y funcionando

```bash
docker --version
```

**Resultado esperado:** `Docker version 24.x.x, build ...` (o superior)

```bash
sudo docker run hello-world
```

**Resultado esperado:** Mensaje de bienvenida de Docker confirmando que funciona correctamente.

### 4.6. Añadir usuario actual al grupo docker (opcional pero recomendado)

**⚠️ ¿Necesito hacer este paso?**

- **Si estás como `root`:** NO necesitas hacer esto. El usuario root ya tiene todos los permisos.
- **Si estás con un usuario normal:** SÍ, hazlo para poder usar Docker sin `sudo` en cada comando.

Para verificar si eres root, ejecuta:
```bash
whoami
```
- Si muestra `root` → Puedes saltar este paso
- Si muestra otro nombre → Ejecuta los comandos siguientes

**Añadir tu usuario al grupo docker:**

```bash
sudo usermod -aG docker $USER
```

**¿Qué hace este comando?**
- `usermod` → Modifica un usuario
- `-aG docker` → Añade (`a`) al grupo (`G`) llamado `docker`
- `$USER` → Variable que contiene tu nombre de usuario actual

**Nota:** Necesitarás cerrar sesión y volver a entrar para que este cambio tenga efecto.

Para aplicar el cambio sin cerrar sesión:

```bash
newgrp docker
```

**Verificar que funcionó:**

```bash
docker ps
```

Si ejecutas este comando sin `sudo` y no da error de permisos, está correcto.

---

## Paso 5: Instalación de Docker Compose

### 5.1. Instalar plugin de Docker Compose

```bash
sudo apt install -y docker-compose-plugin
```

### 5.2. Verificar instalación

```bash
docker compose version
```

**Resultado esperado:** `Docker Compose version v2.x.x` (o superior)

**Nota importante:** Observa que el comando es `docker compose` (con espacio), no `docker-compose` (con guion). La versión moderna de Docker Compose es un plugin, no un binario separado.

---

## Paso 6: Habilitar Docker al arranque

### 6.1. Habilitar servicio Docker

```bash
sudo systemctl enable docker.service
```

### 6.2. Habilitar containerd

```bash
sudo systemctl enable containerd.service
```

### 6.3. Verificar estado de Docker

```bash
sudo systemctl status docker
```

**Resultado esperado:** Estado `active (running)` y que aparezca `enabled` en el arranque.

Presiona `q` para salir de la vista de estado.

### 6.4. Verificar que Docker inicia automáticamente

```bash
sudo systemctl is-enabled docker
```

**Resultado esperado:** `enabled`

---

## Paso 7: Revisar y configurar firewall

### 7.1. Verificar estado del firewall UFW

```bash
sudo ufw status
```

**Posibles resultados:**
- `Status: inactive` → El firewall está desactivado
- `Status: active` → El firewall está activado

### 7.2. Si UFW está inactivo, activarlo

**⚠️ ORDEN CORRECTO DE CONFIGURACIÓN:**

**NO ejecutes `sudo ufw enable` todavía.** Primero debes configurar las reglas de firewall para evitar quedarte sin acceso SSH.

**Sigue estos pasos EN ORDEN:**

1. **Primero:** Configura las reglas (pasos 7.3 y 7.4)
2. **Después:** Activa el firewall (este paso 7.2)

Si ya ejecutaste `sudo ufw enable` y te pregunta:
```
Command may disrupt existing ssh connections. Proceed with operation (y|n)?
```

- **Si NO has permitido el puerto SSH aún:** Presiona `n`, permite el puerto SSH primero (paso 7.3), y luego vuelve aquí.
- **Si YA permitiste el puerto SSH:** Presiona `y` para continuar.

**Comando para activar UFW (solo después de configurar las reglas):**

```bash
sudo ufw enable
```

### 7.3. Permitir puerto SSH (22)

**¿Cómo saber qué puerto SSH estoy usando?**

Por defecto, SSH usa el puerto **22**. Si te has conectado normalmente sin especificar puerto, es el 22.

Para verificarlo con certeza, ejecuta:

```bash
sudo ss -tlnp | grep sshd
```

o también:

```bash
sudo netstat -tlnp | grep sshd
```

Busca una línea que contenga `:22` (o cualquier otro número), ese es tu puerto SSH.

**Ejemplo de salida:**
```
tcp   0   0  0.0.0.0:22     0.0.0.0:*    LISTEN   1234/sshd
```

El número después de los dos puntos (`:22`) es el puerto.

**Otra forma de verificar:**

```bash
cat /etc/ssh/sshd_config | grep "^Port"
```

Si no muestra nada, significa que está usando el puerto por defecto (22).

**Permitir el puerto SSH en el firewall:**

Si tu puerto es el 22 (lo más común):

```bash
sudo ufw allow 22/tcp
```

Si usas otro puerto (por ejemplo, 2222):

```bash
sudo ufw allow 2222/tcp
```

**⚠️ MUY IMPORTANTE:** Debes permitir el puerto SSH **ANTES** de activar UFW, o perderás la conexión al servidor.

### 7.4. Permitir puertos HTTP y HTTPS (necesarios para n8n)

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### 7.5. Verificar reglas del firewall

```bash
sudo ufw status numbered
```

**Resultado esperado:**

```
Status: active

     To                         Action      From
     --                         ------      ----
[ 1] 22/tcp                     ALLOW IN    Anywhere
[ 2] 80/tcp                     ALLOW IN    Anywhere
[ 3] 443/tcp                    ALLOW IN    Anywhere
```

### 7.6. Configuración alternativa con reglas específicas

Si quieres ser más específico, puedes limitar SSH solo a tu IP:

```bash
sudo ufw allow from TU_IP_LOCAL to any port 22 proto tcp
```

### 7.7. Verificar firewall del panel de IONOS

**IMPORTANTE:** IONOS puede tener un firewall adicional a nivel de panel de control. Verifica en:

1. Panel de control de IONOS
2. Sección de tu VPS
3. Opciones de firewall/seguridad
4. Asegúrate de que los puertos 22, 80 y 443 están abiertos

---

## Verificación final

### Checklist de verificación

Ejecuta estos comandos para confirmar que todo está correcto:

#### ✅ Sistema actualizado

```bash
sudo apt update && sudo apt list --upgradable
```

Resultado esperado: `All packages are up to date` o lista vacía.

#### ✅ Docker instalado

```bash
docker --version
```

#### ✅ Docker Compose instalado

```bash
docker compose version
```

#### ✅ Docker funcionando

```bash
sudo systemctl status docker
```

#### ✅ Docker habilitado al arranque

```bash
sudo systemctl is-enabled docker
```

#### ✅ Firewall configurado

```bash
sudo ufw status
```

#### ✅ Permisos de usuario (si aplicaste el paso 4.6)

```bash
docker ps
```

Si ejecutas sin `sudo` y no da error, los permisos están correctos.

### Resumen de la Fase 1

Si todos los checks anteriores están correctos, la **Fase 1 está completada** y tu servidor está listo para la **Fase 2: Preparación de red y acceso**.

---

## Troubleshooting

### Problema: "Permission denied" al ejecutar Docker

**Solución:**

```bash
sudo usermod -aG docker $USER
newgrp docker
```

O simplemente usa `sudo` antes de los comandos Docker.

---

### Problema: "Failed to start docker.service"

**Solución:**

```bash
sudo systemctl restart docker
sudo journalctl -xeu docker.service
```

Revisa los logs para identificar el problema específico.

---

### Problema: No puedo conectarme por SSH después de activar UFW

**Solución:** Necesitarás acceder desde el panel de IONOS (consola VNC) y ejecutar:

```bash
sudo ufw allow 22/tcp
sudo ufw reload
```

---

### Problema: "apt update" falla con errores de repositorio

**Solución:**

```bash
sudo apt update --fix-missing
sudo apt clean
sudo apt update
```

---

### Problema: Docker no se inicia automáticamente después de reiniciar

**Solución:**

```bash
sudo systemctl enable docker.service
sudo systemctl enable containerd.service
sudo systemctl start docker
```

---

### Problema: Firewall de IONOS bloquea puertos aunque UFW esté configurado

**Solución:** Accede al panel de control de IONOS y configura el firewall desde allí. UFW controla el firewall del sistema operativo, pero IONOS puede tener un firewall adicional a nivel de infraestructura.

---

## Comandos de referencia rápida

```bash
# Actualizar sistema
sudo apt update && sudo apt upgrade -y

# Ver versión de Docker
docker --version

# Ver versión de Docker Compose
docker compose version

# Ver estado de Docker
sudo systemctl status docker

# Ver reglas de firewall
sudo ufw status numbered

# Añadir regla al firewall
sudo ufw allow PUERTO/tcp

# Ver logs de Docker
sudo journalctl -xeu docker.service

# Reiniciar Docker
sudo systemctl restart docker

# Ver contenedores en ejecución
docker ps

# Ver todos los contenedores
docker ps -a
```

---

## Próximos pasos

Una vez completada la Fase 1, procede con:

**Fase 2: Preparación de red y acceso**
- Configurar dominio/subdominio
- Comprobar resolución DNS
- Verificar acceso externo a puertos 80 y 443

---

## Notas adicionales

- **Backups:** Considera hacer un snapshot del VPS en este punto desde el panel de IONOS. Así tendrás un punto de restauración limpio.
- **Seguridad:** Considera cambiar el puerto SSH por defecto (22) a otro puerto personalizado para mayor seguridad.
- **Actualizaciones automáticas:** Puedes configurar actualizaciones automáticas de seguridad con `unattended-upgrades`.
- **Monitorización:** Instala herramientas como `htop` para monitorizar recursos: `sudo apt install htop`

---

## Registro de ejecución

Usa esta tabla para documentar cuándo completaste cada paso:

| Paso | Descripción | Fecha | Resultado | Notas |
|------|------------|-------|-----------|-------|
| 1 | Conexión SSH | | | |
| 2 | Actualización de paquetes | | | |
| 3 | Dependencias básicas | | | |
| 4 | Instalación Docker | | | |
| 5 | Instalación Docker Compose | | | |
| 6 | Habilitar Docker al arranque | | | |
| 7 | Configurar firewall | | | |

---

**Fin de la guía de Fase 1**

Documento creado: 16/03/2026  
Última actualización: 16/03/2026
