# Guía Fase 3: Configuración del Dominio s0d1re.es en IONOS

**Proyecto:** Configuración de dominio para n8n en VPS  
**Fase:** 3 - Configuración DNS en IONOS  
**Dominio:** s0d1re.es  
**Proveedor:** IONOS  
**VPS IP:** 212.227.255.246  
**Fecha:** 23/03/2026

---

## 📋 Resumen rápido

**Objetivo:** Configurar el dominio s0d1re.es para que apunte al VPS de IONOS donde está instalado n8n.

**Datos clave:**
- 🌐 **Dominio:** s0d1re.es (registrado en IONOS)
- 🖥️ **IP del VPS:** 212.227.255.246
- 👤 **Usuario VPS:** d4htr95m-agustin
- 📧 **Email cuenta IONOS:** sodire.info@gmail.com
- 🔐 **Contraseña:** Sodire21@

**Lo que vas a configurar:**
- Dominio principal: `s0d1re.es` → 212.227.255.246
- Subdominio para n8n: `n8n.s0d1re.es` → 212.227.255.246
- Subdominio www: `www.s0d1re.es` → 212.227.255.246

**Tiempo estimado:** 20-30 minutos + tiempo de propagación DNS (5-48h)

---

## Índice

1. [Requisitos previos](#requisitos-previos)
2. [Paso 1: Acceder al panel de IONOS](#paso-1-acceder-al-panel-de-ionos)
3. [Paso 2: Localizar la gestión de DNS](#paso-2-localizar-la-gestión-de-dns)
4. [Paso 3: Configurar registros DNS](#paso-3-configurar-registros-dns)
5. [Paso 4: Verificar la configuración](#paso-4-verificar-la-configuración)
6. [Paso 5: Comprobar propagación DNS](#paso-5-comprobar-propagación-dns)
7. [Paso 6: Configurar firewall IONOS](#paso-6-configurar-firewall-ionos)
8. [Paso 7: Configurar firewall UFW en el VPS](#paso-7-configurar-firewall-ufw-en-el-vps)
9. [Verificación final](#verificación-final)
10. [Troubleshooting](#troubleshooting)

---

## Requisitos previos

Antes de comenzar, asegúrate de tener:

- ✅ Cuenta de IONOS activa (sodire.info@gmail.com)
- ✅ Contraseña de acceso al panel de IONOS
- ✅ Dominio s0d1re.es registrado en IONOS
- ✅ VPS Linux activo en IONOS
- ✅ IP del VPS: 212.227.255.246
- ✅ Acceso SSH al VPS

---

## Paso 1: Acceder al panel de IONOS

### 1.1. Abrir el panel de IONOS

1. Abre tu navegador
2. Ve a: **https://my.ionos.es**
3. Inicia sesión con:
   - **Email:** sodire.info@gmail.com
   - **Contraseña:** Sodire21@

### 1.2. Verificar acceso

Una vez dentro, deberías ver el panel principal de IONOS con tus servicios contratados.

**Deberías ver:**
- Dominios contratados
- Servidores VPS
- Otros servicios

---

## Paso 2: Localizar la gestión de DNS

### 2.1. Acceder a la gestión de dominios

Desde el panel principal de IONOS:

1. Busca en el menú lateral o superior la opción **"Dominios"** o **"Dominios y SSL"**
2. Haz clic en **"Dominios"**
3. Deberías ver una lista de tus dominios, incluyendo **s0d1re.es**

### 2.2. Seleccionar el dominio s0d1re.es

1. En la lista de dominios, localiza **s0d1re.es**
2. Haz clic sobre el dominio o en el icono de configuración (⚙️) junto a él
3. Busca la opción **"DNS"** o **"Configuración DNS"** o **"Gestionar DNS"**

**Alternativa:**
- Puede que veas un botón que dice **"Administrar"** o **"Gestionar"**
- Al hacer clic, deberías ver opciones como:
  - Configuración DNS
  - Redirecciones
  - Subdominios
  - etc.

### 2.3. Acceder a la configuración DNS

1. Haz clic en **"DNS"** o **"Configuración DNS"**
2. Deberías ver la pantalla de gestión de registros DNS

**Importante:**
- Si te pregunta si quieres usar los **servidores DNS de IONOS** o servidores externos, elige **"Usar DNS de IONOS"**
- Esto te permitirá gestionar los registros directamente desde el panel

---

## Paso 3: Configurar registros DNS

### 3.1. Entender los registros DNS que necesitas

Vas a crear los siguientes registros:

| Tipo | Nombre/Host | Valor/Destino | TTL | Propósito |
|------|-------------|---------------|-----|-----------|
| A | @ o s0d1re.es | 212.227.255.246 | 3600 | Dominio principal |
| A | www | 212.227.255.246 | 3600 | Subdominio www |
| A | n8n | 212.227.255.246 | 3600 | Subdominio para n8n |

**Explicación:**
- **Tipo A:** Apunta un dominio/subdominio a una dirección IP
- **@:** Representa el dominio raíz (s0d1re.es)
- **www:** Subdominio www (www.s0d1re.es)
- **n8n:** Subdominio para acceder a n8n (n8n.s0d1re.es)
- **TTL:** Time To Live - tiempo de caché (3600 = 1 hora)

### 3.2. Eliminar registros DNS antiguos o conflictivos (si existen)

Antes de añadir nuevos registros, **revisa los registros existentes**:

1. Busca si ya existen registros A para:
   - @ o el dominio raíz
   - www
   - n8n
   - * (comodín)

2. **Elimina o modifica** los registros que apunten a otras IPs o servicios

**Importante:**
- **NO elimines** registros tipo MX (correo electrónico) a menos que sepas lo que haces
- **NO elimines** registros TXT (pueden ser importantes para verificaciones)
- **NO elimines** registros NS (servidores de nombres)

### 3.3. Crear registro A para el dominio principal

1. En la gestión de DNS, busca el botón **"Añadir"** o **"Añadir registro"**
2. Selecciona tipo de registro: **A**
3. Rellena los campos:
   - **Nombre/Host/Subdominio:** @ (o déjalo vacío, o escribe "s0d1re.es")
   - **Tipo:** A
   - **Valor/IP/Destino:** 212.227.255.246
   - **TTL:** 3600 (o déjalo por defecto)
   - **Prioridad:** (no aplica para registros A)
4. Haz clic en **"Guardar"** o **"Añadir"**

**Resultado esperado:**
```
s0d1re.es. → 212.227.255.246
```

### 3.4. Crear registro A para www

1. Haz clic nuevamente en **"Añadir registro"**
2. Rellena:
   - **Nombre/Host:** www
   - **Tipo:** A
   - **Valor/IP:** 212.227.255.246
   - **TTL:** 3600
3. Guarda

**Resultado esperado:**
```
www.s0d1re.es. → 212.227.255.246
```

### 3.5. Crear registro A para n8n (subdominio para n8n)

1. Añadir un nuevo registro
2. Rellena:
   - **Nombre/Host:** n8n
   - **Tipo:** A
   - **Valor/IP:** 212.227.255.246
   - **TTL:** 3600
3. Guarda

**Resultado esperado:**
```
n8n.s0d1re.es. → 212.227.255.246
```

### 3.6. (Opcional) Crear registro CNAME para www como alternativa

**Alternativa al registro A para www:**

En lugar de crear un registro A para www, puedes crear un registro CNAME:

- **Nombre/Host:** www
- **Tipo:** CNAME
- **Valor/Destino:** s0d1re.es. (con punto al final)
- **TTL:** 3600

**Ventaja:** Si cambias la IP del VPS, solo necesitas actualizar el registro A principal.

**Nota:** No puedes tener un registro A y un CNAME para el mismo nombre. Elige uno u otro.

### 3.7. Revisar la configuración final

Después de añadir todos los registros, deberías ver algo así:

**Registros DNS de s0d1re.es:**

```
Tipo  | Nombre/Host | Valor/Destino      | TTL
------|-------------|--------------------|----- 
A     | @           | 212.227.255.246    | 3600
A     | www         | 212.227.255.246    | 3600
A     | n8n         | 212.227.255.246    | 3600
```

O si usaste CNAME para www:

```
Tipo  | Nombre/Host | Valor/Destino      | TTL
------|-------------|--------------------|----- 
A     | @           | 212.227.255.246    | 3600
CNAME | www         | s0d1re.es.         | 3600
A     | n8n         | 212.227.255.246    | 3600
```

---

## Paso 4: Verificar la configuración

### 4.1. Guardar cambios

Asegúrate de hacer clic en **"Guardar cambios"** o **"Aplicar"** si es necesario.

Algunos paneles guardan automáticamente cada registro, otros requieren un guardado final.

### 4.2. Confirmar en el panel

Revisa que los registros aparezcan correctamente en la lista de registros DNS.

---

## Paso 5: Comprobar propagación DNS

### 5.1. Entender la propagación DNS

Los cambios en DNS **no son inmediatos**. Pueden tardar:
- **Mínimo:** 5-15 minutos
- **Normal:** 1-4 horas
- **Máximo:** 24-48 horas

Esto depende de:
- El TTL configurado
- Los cachés de DNS intermedios
- Tu proveedor de Internet

### 5.2. Comprobar DNS desde tu ordenador (Windows)

Abre **PowerShell** o **CMD** y ejecuta:

```powershell
nslookup s0d1re.es
```

**Resultado esperado (una vez propagado):**
```
Nombre: s0d1re.es
Address: 212.227.255.246
```

También comprueba los subdominios:

```powershell
nslookup www.s0d1re.es
nslookup n8n.s0d1re.es
```

### 5.3. Comprobar DNS desde el VPS

Conéctate al VPS por SSH:

```bash
ssh d4htr95m-agustin@212.227.255.246
```

Ejecuta:

```bash
nslookup s0d1re.es
```

```bash
dig s0d1re.es +short
```

**Resultado esperado:**
```
212.227.255.246
```

### 5.4. Comprobar DNS online

Usa herramientas online para verificar la propagación:

1. **https://dnschecker.org**
   - Introduce: s0d1re.es
   - Tipo: A
   - Haz clic en "Search"
   - Verás si el dominio apunta a 212.227.255.246 desde diferentes ubicaciones

2. **https://www.whatsmydns.net**
   - Introduce: s0d1re.es
   - Tipo: A
   - Comprueba la propagación global

3. **https://mxtoolbox.com/DNSLookup.aspx**
   - Introduce: s0d1re.es
   - Verifica los registros

### 5.5. ¿Qué hacer mientras esperas la propagación?

La propagación puede tardar unas horas. Mientras tanto, puedes:

1. ✅ Continuar con la configuración del firewall
2. ✅ Preparar la configuración de n8n con el dominio
3. ✅ Preparar la configuración de certificados SSL
4. ☕ Tomar un café

**Nota:** Aunque la propagación puede tardar 48h, normalmente en 1-4 horas ya funciona.

---

## Paso 6: Configurar firewall IONOS

IONOS tiene un **firewall a nivel de red** que debes configurar en el panel web.

### 6.1. Acceder al panel del VPS en IONOS

1. En el panel de IONOS (https://my.ionos.es)
2. Ve a la sección de **"Servidores"** o **"VPS"**
3. Localiza tu VPS (IP: 212.227.255.246)
4. Haz clic sobre él para ver los detalles

### 6.2. Acceder a la configuración del firewall

1. Dentro de la configuración del VPS, busca:
   - **"Firewall"**
   - **"Seguridad"**
   - **"Red y seguridad"**
   - O similar

2. Haz clic en **"Firewall"**

### 6.3. Configurar reglas del firewall

Debes permitir el tráfico en los siguientes puertos:

| Puerto | Protocolo | Servicio | Descripción |
|--------|-----------|----------|-------------|
| 22 | TCP | SSH | Acceso SSH al servidor |
| 80 | TCP | HTTP | Tráfico web sin cifrar |
| 443 | TCP | HTTPS | Tráfico web cifrado (SSL) |
| 5678 | TCP | n8n | Puerto de n8n (temporal, luego se cerrará) |

### 6.4. Añadir reglas

**Para cada puerto, crea una regla:**

1. Haz clic en **"Añadir regla"** o **"Nueva regla"**
2. Rellena:
   - **Protocolo:** TCP
   - **Puerto:** (el número del puerto, ej: 22)
   - **Origen:** 0.0.0.0/0 (cualquier IP) o "Anywhere"
   - **Acción:** Permitir / Allow / Accept
   - **Descripción:** SSH / HTTP / HTTPS / n8n

**Ejemplo para el puerto 22 (SSH):**
```
Protocolo: TCP
Puerto: 22
Origen: 0.0.0.0/0
Acción: Permitir
Descripción: SSH
```

**Ejemplo para el puerto 80 (HTTP):**
```
Protocolo: TCP
Puerto: 80
Origen: 0.0.0.0/0
Acción: Permitir
Descripción: HTTP
```

**Ejemplo para el puerto 443 (HTTPS):**
```
Protocolo: TCP
Puerto: 443
Origen: 0.0.0.0/0
Acción: Permitir
Descripción: HTTPS
```

**Ejemplo para el puerto 5678 (n8n - temporal):**
```
Protocolo: TCP
Puerto: 5678
Origen: 0.0.0.0/0
Acción: Permitir
Descripción: n8n temporal
```

### 6.5. Guardar y aplicar cambios

1. Asegúrate de guardar todas las reglas
2. Puede que tengas que hacer clic en **"Aplicar cambios"** o **"Activar"**
3. Las reglas deberían aplicarse en unos segundos

### 6.6. Verificar reglas creadas

Revisa que las 4 reglas (puertos 22, 80, 443, 5678) estén activas y correctamente configuradas.

---

## Paso 7: Configurar firewall UFW en el VPS

Además del firewall de IONOS, el VPS Linux tiene su propio firewall: **UFW**.

### 7.1. Conectarse al VPS por SSH

```bash
ssh d4htr95m-agustin@212.227.255.246
```

Cuando te pida la contraseña, introduce: **QY8ON5vAwioNVj2**

### 7.2. Verificar estado de UFW

```bash
sudo ufw status
```

**Si está inactivo:**
```
Status: inactive
```

**Si está activo:**
```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
...
```

### 7.3. Configurar reglas UFW (si es necesario)

**Si UFW está inactivo y quieres activarlo:**

**⚠️ IMPORTANTE:** Antes de activar UFW, asegúrate de permitir SSH para no perder el acceso.

```bash
# Permitir SSH (puerto 22)
sudo ufw allow 22/tcp

# Permitir HTTP (puerto 80)
sudo ufw allow 80/tcp

# Permitir HTTPS (puerto 443)
sudo ufw allow 443/tcp

# Permitir n8n (puerto 5678) - temporal
sudo ufw allow 5678/tcp
```

### 7.4. Activar UFW (si está desactivado)

```bash
sudo ufw enable
```

Te preguntará si estás seguro. Escribe `y` y presiona Enter.

**Advertencia que verás:**
```
Command may disrupt existing ssh connections. Proceed with operation (y|n)?
```

Escribe `y` (porque ya has permitido el puerto 22).

### 7.5. Verificar reglas UFW

```bash
sudo ufw status verbose
```

**Resultado esperado:**
```
Status: active
Logging: on (low)
Default: deny (incoming), allow (outgoing), disabled (routed)
New profiles: skip

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW IN    Anywhere
80/tcp                     ALLOW IN    Anywhere
443/tcp                    ALLOW IN    Anywhere
5678/tcp                   ALLOW IN    Anywhere
22/tcp (v6)                ALLOW IN    Anywhere (v6)
80/tcp (v6)                ALLOW IN    Anywhere (v6)
443/tcp (v6)              ALLOW IN    Anywhere (v6)
5678/tcp (v6)              ALLOW IN    Anywhere (v6)
```

### 7.6. (Opcional) Si UFW ya estaba configurado

Si UFW ya estaba activo y con reglas, simplemente verifica que los puertos 22, 80, 443 estén permitidos:

```bash
sudo ufw status
```

Si falta algún puerto, añádelo:

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

---

## Verificación final

### ✅ Checklist de verificación

Marca cada punto según lo vayas completando:

**Configuración DNS:**
- [ ] Registro A para @ o s0d1re.es apunta a 212.227.255.246
- [ ] Registro A para www apunta a 212.227.255.246
- [ ] Registro A para n8n apunta a 212.227.255.246
- [ ] Cambios guardados en el panel de IONOS
- [ ] DNS propagado (verificado con nslookup o dnschecker.org)

**Firewall IONOS (panel web):**
- [ ] Puerto 22 (SSH) permitido
- [ ] Puerto 80 (HTTP) permitido
- [ ] Puerto 443 (HTTPS) permitido
- [ ] Puerto 5678 (n8n temporal) permitido
- [ ] Reglas guardadas y activas

**Firewall UFW (VPS):**
- [ ] UFW activo o configurado
- [ ] Puerto 22 permitido
- [ ] Puerto 80 permitido
- [ ] Puerto 443 permitido
- [ ] Puerto 5678 permitido (temporal)

**Pruebas de conectividad:**
- [ ] `nslookup s0d1re.es` devuelve 212.227.255.246
- [ ] `nslookup www.s0d1re.es` devuelve 212.227.255.246
- [ ] `nslookup n8n.s0d1re.es` devuelve 212.227.255.246
- [ ] Puedes conectarte por SSH al VPS
- [ ] Puedes acceder a http://212.227.255.246:5678 (n8n)

---

## Troubleshooting

### ❌ Problema: Los cambios DNS no se propagan

**Síntoma:**
```powershell
nslookup s0d1re.es
# No devuelve 212.227.255.246
```

**Soluciones:**

1. **Espera más tiempo:** La propagación puede tardar hasta 48h
2. **Limpia la caché DNS de tu ordenador:**
   ```powershell
   ipconfig /flushdns
   ```
3. **Verifica en dnschecker.org:** Puede que esté propagado en otros lugares pero no en tu zona
4. **Revisa los registros en IONOS:** Asegúrate de que están correctos y guardados
5. **Verifica que estés usando los DNS de IONOS:** No DNS externos

### ❌ Problema: No puedo acceder al VPS por SSH

**Síntoma:**
```bash
ssh d4htr95m-agustin@212.227.255.246
# Connection refused o timeout
```

**Soluciones:**

1. **Verifica el firewall de IONOS:** Asegúrate de que el puerto 22 está permitido
2. **Verifica UFW en el VPS:**
   - Si tienes acceso desde la consola web de IONOS, verifica UFW
   - Si no, usa la consola web de IONOS para desactivar UFW o añadir la regla
3. **Verifica la IP del VPS:**
   ```bash
   # Desde el VPS (consola web IONOS)
   curl ifconfig.me
   ```
4. **Prueba con la consola web de IONOS:** Accede al VPS desde el panel web

### ❌ Problema: No puedo acceder a http://s0d1re.es

**Síntoma:** El navegador muestra "No se puede acceder al sitio" o timeout

**Soluciones:**

1. **Verifica que el DNS esté propagado:**
   ```powershell
   nslookup s0d1re.es
   ```
2. **Verifica los firewalls:**
   - Puerto 80 permitido en firewall IONOS
   - Puerto 80 permitido en UFW
3. **Verifica que haya un servicio escuchando en el puerto 80:**
   ```bash
   # Desde el VPS
   sudo ss -tlnp | grep :80
   ```
   - Si no hay nada, es normal: aún no has configurado un servidor web
   - Esto lo harás en la siguiente fase con Caddy o Nginx

4. **Prueba acceder por IP:**
   ```
   http://212.227.255.246
   ```

### ❌ Problema: El firewall de IONOS no tiene opción de configuración

**Posibles causas:**

1. Algunos planes de VPS de IONOS no tienen firewall configurable desde el panel
2. El firewall puede estar gestionado automáticamente

**Solución:**

- Si no encuentras la opción de firewall en el panel de IONOS, no te preocupes
- IONOS puede tener los puertos abiertos por defecto
- Concéntrate en configurar UFW en el VPS, que es lo más importante
- Contacta con soporte de IONOS si tienes dudas

### ❌ Problema: nslookup dice "can't find s0d1re.es: Non-existent domain"

**Causa:** Los registros DNS aún no están propagados o no están correctamente configurados

**Soluciones:**

1. **Verifica en el panel de IONOS:** Asegúrate de que los registros están creados
2. **Espera más tiempo:** Puede tardar varias horas
3. **Limpia la caché DNS:**
   ```powershell
   ipconfig /flushdns
   ```
4. **Usa otro servidor DNS para la consulta:**
   ```powershell
   nslookup s0d1re.es 8.8.8.8
   ```
   (8.8.8.8 es el DNS de Google)

5. **Verifica que los servidores DNS estén configurados:**
   ```powershell
   nslookup -type=NS s0d1re.es
   ```
   Deberías ver los servidores de nombres de IONOS

---

## 🎯 Próximos pasos

Una vez completada esta fase (configuración de dominio y firewall), estarás listo para:

**Fase 4: Instalación y configuración de n8n con dominio**
- Configurar proxy inverso (Caddy o Nginx)
- Obtener certificado SSL automático para s0d1re.es y n8n.s0d1re.es
- Configurar n8n para usar el dominio en lugar de la IP
- Cerrar el acceso directo al puerto 5678

**Fase 5: Optimización y seguridad**
- Configurar backups automáticos
- Configurar actualizaciones automáticas
- Endurecer la seguridad del VPS
- Optimizar el rendimiento de n8n

---

## 📚 Recursos adicionales

**Documentación oficial:**
- IONOS DNS: https://www.ionos.es/ayuda/dominios/
- UFW: https://help.ubuntu.com/community/UFW

**Herramientas útiles:**
- DNS Checker: https://dnschecker.org
- What's My DNS: https://www.whatsmydns.net
- MX Toolbox: https://mxtoolbox.com

**Soporte:**
- Soporte IONOS: https://www.ionos.es/ayuda/
- Teléfono IONOS España: 911 23 85 61

---

## 📝 Notas finales

**Importante:**
- El puerto 5678 de n8n es temporal. Una vez configures el proxy inverso con SSL, cerrarás este puerto.
- Guarda esta documentación y los datos de acceso en un lugar seguro.
- Haz backups regulares de la configuración de DNS.

**Tiempo total estimado:**
- Configuración DNS: 10-15 minutos
- Propagación DNS: 1-4 horas (puede llegar a 48h)
- Configuración firewall: 10-15 minutos
- **Total activo:** 20-30 minutos
- **Total con espera:** 1-4 horas

---

**Guía creada:** 23/03/2026  
**Última actualización:** 23/03/2026  
**Versión:** 1.0
