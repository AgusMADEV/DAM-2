# Guía Fase 2: Preparación de Red y Acceso

**Proyecto:** Instalación de n8n en VPS  
**Fase:** 2 - Preparación de red y acceso  
**Sistema:** Ubuntu Server (IONOS VPS)  
**Dominio:** sodire.es (gestionado en Cloudflare)  
**Subdominio para n8n:** n8n.sodire.es  
**Fecha:** 16/03/2026

---

> **📌 Configuración específica de este proyecto:**
> 
> - 🏢 **Proveedor VPS:** IONOS (VPS Linux Ubuntu)
> - 🌐 **Dominio:** sodire.es
> - ☁️ **DNS gestionado en:** Cloudflare
> - 🔧 **Subdominio para n8n:** n8n.sodire.es
> - 🔒 **Firewall:** Doble nivel (UFW + Panel IONOS)
> 
> **Accesos importantes:**
> - Panel IONOS: https://my.ionos.es
> - Panel Cloudflare: https://dash.cloudflare.com

---

## Índice

1. [Requisitos previos](#requisitos-previos)
2. [Paso 1: Obtener información del servidor](#paso-1-obtener-información-del-servidor)
3. [Paso 2: Decidir sobre el dominio](#paso-2-decidir-sobre-el-dominio)
4. [Paso 3: Configurar dominio/subdominio](#paso-3-configurar-dominiosubdominio)
5. [Paso 4: Comprobar resolución DNS](#paso-4-comprobar-resolución-dns)
6. [Paso 5: Verificar puertos abiertos](#paso-5-verificar-puertos-abiertos)
7. [Paso 6: Verificar acceso externo](#paso-6-verificar-acceso-externo)
8. [Verificación final](#verificación-final)
9. [Troubleshooting](#troubleshooting)

---

## Requisitos previos

Antes de comenzar esta fase, debes haber completado:

- ✅ **Fase 1:** Preparación del servidor (Docker instalado y firewall configurado)
- ✅ Acceso SSH al VPS IONOS
- ✅ La IP pública de tu VPS IONOS

**Nuevos requisitos para esta fase:**

- 🔲 Dominio propio (opcional pero muy recomendado)
- 🔲 Acceso al panel de gestión DNS de tu dominio
- 🔲 Conocer la IP pública del VPS
- 🔲 Acceso al panel de control de IONOS (https://my.ionos.es)

**Nota importante sobre IONOS:**

IONOS VPS Linux incluye dos niveles de firewall:
1. **UFW (Uncomplicated Firewall)** - A nivel del sistema operativo Ubuntu
2. **Firewall de IONOS** - A nivel del panel de control web

Ambos deben estar correctamente configurados para que n8n funcione.

---

## 📋 Resumen rápido: Tu configuración

Si quieres ir directo al grano, aquí está lo que vas a hacer en esta fase:

**Tu configuración específica:**
- ✅ VPS: IONOS Linux Ubuntu
- ✅ Dominio: sodire.es (ya lo tienes)
- ✅ DNS: Cloudflare (ya configurado)
- ⚙️ Crear: n8n.sodire.es → IP del VPS

**Pasos principales:**

1. **Obtener IP del VPS:** `curl ifconfig.me`
2. **Ir a Cloudflare** → DNS → Añadir registro A
3. **Configurar:** n8n → Tu IP → DNS only (gris)
4. **Verificar:** `nslookup n8n.sodire.es`
5. **Firewall UFW:** Puertos 22, 80, 443
6. **Firewall IONOS:** Panel web → Puertos 22, 80, 443

**Tiempo estimado:** 15-20 minutos

---

## Paso 1: Obtener información del servidor

### 1.1. Confirmar IP pública del VPS

Desde tu servidor VPS, ejecuta:

```bash
curl ifconfig.me
```

o también:

```bash
curl icanhazip.com
```

**Resultado esperado:** Tu IP pública

**Anota esta IP**, la necesitarás para configurar el DNS.

### 1.2. Verificar puerto SSH

```bash
sudo ss -tlnp | grep sshd
```

**Resultado esperado:** Confirmar que SSH está en el puerto 22 (o el que uses).

### 1.3. Verificar hostname actual

```bash
hostname
```

**Ejemplo de resultado:** `modest-napier.212-227-159-22.plesk.page`

---

## Paso 2: Decidir sobre el dominio

> **✅ Para este proyecto: Ya está decidido**
> 
> Vas a usar: **n8n.sodire.es**
> - Dominio base: sodire.es (ya lo tienes)
> - Gestionado en: Cloudflare
> - Acción: Crear subdominio n8n
> 
> Puedes **saltar al Paso 3** directamente o leer las opciones a continuación para entender por qué esta es la mejor elección.

Tienes **3 opciones** para acceder a n8n:

### Opción A: Usar un dominio propio (RECOMENDADO)

**Ventajas:**
- ✅ Certificado SSL automático con Let's Encrypt
- ✅ Fácil de recordar y profesional
- ✅ Configuración más limpia

**Requisitos:**
- Tener un dominio registrado (ej: `midominio.com`)
- Acceso al panel DNS del dominio

**Ejemplos:**
- `n8n.midominio.com`
- `automatizacion.midominio.com`
- `workflows.midominio.com`

**¿Dónde conseguir un dominio?**
- Namecheap
- Google Domains
- Cloudflare
- GoDaddy
- El propio IONOS

**Coste aproximado:** 10-15€/año

---

### Opción B: Usar un subdominio gratuito (TEMPORAL)

**Servicios gratuitos:**
- DuckDNS (*.duckdns.org)
- FreeDNS (afraid.org)
- No-IP

**Ventajas:**
- ✅ Gratis
- ✅ Funciona con Let's Encrypt

**Desventajas:**
- ⚠️ No es profesional
- ⚠️ Puede tener restricciones

**Ejemplo:** `minombre.duckdns.org`

---

### Opción C: Acceso directo por IP (NO RECOMENDADO para producción)

**Solo para pruebas o desarrollo.**

**Ventajas:**
- ✅ No necesitas dominio
- ✅ Configuración más rápida

**Desventajas:**
- ❌ Sin HTTPS (inseguro)
- ❌ Difícil de recordar
- ❌ Algunos navegadores bloquean funcionalidades
- ❌ No apto para webhooks externos

**Acceso:** `http://TU_IP:5678` (puerto por defecto de n8n)

---

## Paso 3: Configurar n8n.sodire.es en Cloudflare

> **📌 Tu tarea en este paso:**
> Crear un registro DNS tipo A en Cloudflare que apunte **n8n.sodire.es** a la IP de tu VPS IONOS.

---

agusma### 3.1. Acceder a Cloudflare DNS

1. Ve a https://dash.cloudflare.com
2. Login con tus credenciales de Cloudflare
3. Selecciona el dominio **sodire.es** de la lista
4. En el menú lateral, haz clic en **DNS** → **Records**

### 3.2. Añadir registro DNS tipo A para n8n

Haz clic en **Add record** y configura:

**Configuración recomendada para n8n.sodire.es:**

```
Type: A
Name: n8n
IPv4 address: [Tu IP del VPS IONOS - obtén con: curl ifconfig.me]
Proxy status: DNS only (🌐 nube GRIS, NO naranja)
TTL: Auto
```

**Ejemplo práctico con tu IP:**

Si tu IP del VPS es `212.227.159.22`:

```
Type: A
Name: n8n
IPv4 address: 212.227.159.22
Proxy status: DNS only (nube gris)
TTL: Auto
```

Esto creará: **n8n.sodire.es** → Tu IP del VPS

### 3.3. Guardar el registro

1. Haz clic en **Save**
2. El registro aparecerá en la lista inmediatamente
3. La propagación en Cloudflare es casi instantánea (2-5 minutos)

### 3.4. ⚠️ MUY IMPORTANTE: Proxy Status

**Deja el proxy DESACTIVADO** (nube gris 🌐, **NO** naranja 🟠)

**¿Por qué?**

- Let's Encrypt necesita acceso directo a tu VPS para validar el dominio
- Si activas el proxy naranja, Caddy no podrá generar el certificado SSL
- **Después de que Caddy genere el certificado**, si quieres, puedes activar el proxy (Fase 4)

**Estado correcto:**
```
n8n.sodire.es  |  A  |  212.227.159.22  |  🌐 DNS only  |  Auto
```

**Estado INCORRECTO (no usar inicialmente):**
```
n8n.sodire.es  |  A  |  212.227.159.22  |  🟠 Proxied  |  Auto
```

### 3.5. Verificar el registro creado

Deberías ver algo como esto en la lista de DNS:

| Type | Name | Content | Proxy status | TTL |
|------|------|---------|--------------|-----|
| A | n8n | 212.227.159.22 | DNS only | Auto |

### 3.6. Configuración SSL/TLS de Cloudflare (verificar)

Ve a **SSL/TLS** en el menú lateral y asegúrate de que:

- **SSL/TLS encryption mode** está en **Full** o **Full (strict)**
- NO uses **Flexible** (dará problemas con Caddy)

**Configuración recomendada:**
```
SSL/TLS encryption mode: Full (strict)
```

Esto lo configuraremos mejor en la Fase 4, pero es bueno verificarlo ahora.

**⚠️ IMPORTANTE:** Deja el proxy **desactivado** (nube gris) para que Let's Encrypt pueda validar el dominio.

#### 3.2. Verificar

Espera 2-5 minutos y verifica que el registro aparece en la lista.

---

## Paso 4: Comprobar resolución DNS

Una vez configurado el dominio en Cloudflare, debes verificar que **n8n.sodire.es** apunta correctamente a tu VPS.

### 4.1. Verificación desde tu ordenador local (Windows)

Abre PowerShell o CMD y ejecuta:

```powershell
nslookup n8n.sodire.es
```

**Resultado esperado:**

```
Server:  UnKnown
Address:  192.168.1.1

Non-authoritative answer:
Name:    n8n.sodire.es
Address:  212.227.159.22
```

La IP debe coincidir con la de tu VPS IONOS (la que obtuviste con `curl ifconfig.me`).

### 4.2. Verificación alternativa con ping

```powershell
ping n8n.sodire.es
```

**Resultado esperado:**

```
Pinging n8n.sodire.es [212.227.159.22] with 32 bytes of data:
Reply from 212.227.159.22: bytes=32 time=25ms TTL=54
```

**Nota:** Si Cloudflare tiene el proxy activado (naranja), el ping puede fallar o mostrar una IP de Cloudflare. Por eso recomendamos dejarlo en gris (DNS only).

### 4.3. Desde el servidor VPS IONOS

Conéctate al VPS por SSH y ejecuta:

```bash
dig n8n.sodire.es
```

o si no tienes `dig` instalado:

```bash
nslookup n8n.sodire.es
```

**Resultado esperado:** La IP de tu VPS IONOS.

### 4.4. Verificación online de propagación DNS

Usa herramientas online para verificar que **n8n.sodire.es** resuelve correctamente desde diferentes ubicaciones del mundo:

**Herramientas recomendadas:**

1. **DNSChecker** - https://dnschecker.org
   - Introduce: `n8n.sodire.es`
   - Selecciona tipo: **A**
   - Verifica que resuelve a tu IP en múltiples ubicaciones

2. **What's My DNS** - https://www.whatsmydns.net
   - Introduce: `n8n.sodire.es`
   - Verifica propagación global

**¿Cuánto tarda la propagación con Cloudflare?**

- Cloudflare es **muy rápido**: 2-5 minutos normalmente
- Si no resuelve después de 10 minutos, revisa la configuración en Cloudflare
- Otros proveedores DNS pueden tardar hasta 24-48 horas

**Resultado esperado en DNSChecker:**

Deberías ver **verde ✓** en la mayoría de ubicaciones con tu IP del VPS.

---

## Paso 5: Verificar puertos abiertos

### 5.1. Verificar firewall UFW en el servidor

Conéctate al VPS y ejecuta:

```bash
sudo ufw status
```

**Resultado esperado:**

```
Status: active

To                         Action      From
--                         ------      ----
22/tcp                     ALLOW       Anywhere
80/tcp                     ALLOW       Anywhere
443/tcp                    ALLOW       Anywhere
```

Si los puertos 80 y 443 NO están abiertos, ábrelos:

```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
```

### 5.2. Verificar que los puertos están escuchando

```bash
sudo ss -tlnp | grep -E ':(80|443)'
```

**Nota:** Por ahora no habrá nada escuchando en estos puertos (es normal). Los servicios se levantarán en las fases siguientes.

### 5.3. Verificar y configurar firewall de IONOS (panel web)

**⚠️ MUY IMPORTANTE:** IONOS tiene un firewall adicional a nivel de panel de control que es **independiente de UFW**. Aunque UFW esté configurado correctamente, si el firewall de IONOS bloquea los puertos, no podrás acceder.

#### Paso a paso para configurar el firewall de IONOS:

**1. Acceder al panel de IONOS:**

- Ve a https://my.ionos.es
- Inicia sesión con tus credenciales

**2. Localizar tu VPS:**

- En el menú principal, busca **"Servidor y Cloud"** o **"VPS"**
- Selecciona tu VPS de la lista

**3. Acceder a la configuración de Firewall:**

- Busca la pestaña o sección **"Red"** o **"Firewall"**
- Puede estar en:
  - **Configuración** → **Red** → **Firewall**
  - O directamente en **"Firewall"** en el menú lateral

**4. Configurar reglas del firewall:**

Debe haber una sección para añadir reglas. Asegúrate de tener estas reglas:

**Configuración requerida:**

| Nombre | Protocolo | Puerto | Dirección | Origen | Acción |
|--------|-----------|--------|-----------|--------|--------|
| SSH | TCP | 22 | Entrada | 0.0.0.0/0 | Permitir |
| HTTP | TCP | 80 | Entrada | 0.0.0.0/0 | Permitir |
| HTTPS | TCP | 443 | Entrada | 0.0.0.0/0 | Permitir |

**5. Guardar y aplicar cambios:**

- Haz clic en **"Guardar"** o **"Aplicar cambios"**
- Los cambios suelen ser inmediatos (1-2 minutos)

**6. Verificar que las reglas están activas:**

- Refresca la página del firewall
- Confirma que las 3 reglas aparecen como **activas** o **enabled**

**Notas importantes sobre el firewall de IONOS:**

- Por defecto, algunos VPS de IONOS vienen con el firewall desactivado o muy permisivo
- Otros vienen con reglas muy restrictivas que debes modificar
- Si cambias algo y pierdes acceso SSH, puedes usar la **consola VNC** desde el panel de IONOS
- La consola VNC te permite acceder aunque el firewall bloquee SSH

---

## Paso 6: Verificar acceso externo

### 6.1. Probar conectividad HTTP desde fuera

Desde tu ordenador local (NO desde el VPS), ejecuta:

```powershell
Test-NetConnection -ComputerName TU_IP_VPS -Port 80
```

**Resultado esperado:**

```
TcpTestSucceeded : True
```

Si da **False**, el puerto 80 está bloqueado (revisa firewall de IONOS).

### 6.2. Probar puerto 443 (HTTPS)

```powershell
Test-NetConnection -ComputerName TU_IP_VPS -Port 443
```

**Resultado esperado:**

```
TcpTestSucceeded : True
```

### 6.3. Verificación desde herramienta online

Usa herramientas online para verificar que los puertos están abiertos:

- https://www.yougetsignal.com/tools/open-ports/
- https://portchecker.co/

Introduce:
- Tu IP pública del VPS
- Puerto 80 y 443

**Resultado esperado:** Ambos puertos deben aparecer como **abiertos**.

**Nota:** Es posible que mencionen que "no hay servicio escuchando" (es normal por ahora). Lo importante es que NO estén bloqueados.

---

## Verificación final

### Checklist de la Fase 2

Marca cada punto cuando esté completado:

#### ✅ Información del servidor

```bash
curl ifconfig.me
```

- [ ] IP pública obtenida y anotada

#### ✅ Dominio configurado en Cloudflare

- [ ] Subdominio elegido: **n8n.sodire.es**
- [ ] Registro DNS tipo A creado en Cloudflare
- [ ] IP del VPS IONOS configurada en el registro A
- [ ] Proxy status: **DNS only** (nube gris, no naranja)

#### ✅ Resolución DNS verificada

```powershell
nslookup n8n.sodire.es
```

- [ ] n8n.sodire.es resuelve correctamente a la IP del VPS IONOS
- [ ] Verificado desde múltiples ubicaciones (dnschecker.org)
- [ ] Propagación completada (normalmente 2-5 minutos con Cloudflare)

#### ✅ Puertos configurados

```bash
sudo ufw status
```

- [ ] Puerto 22 (SSH) abierto en UFW
- [ ] Puerto 80 (HTTP) abierto en UFW
- [ ] Puerto 443 (HTTPS) abierto en UFW
- [ ] Firewall del panel IONOS verificado y configurado

#### ✅ Acceso externo verificado

```powershell
Test-NetConnection -ComputerName n8n.sodire.es -Port 80
Test-NetConnection -ComputerName n8n.sodire.es -Port 443
```

- [ ] Puerto 80 accesible desde fuera
- [ ] Puerto 443 accesible desde fuera

---

### Resumen de la Fase 2

Si todos los checks anteriores están correctos:

✅ **La Fase 2 está completada**

Tu servidor está listo para:
- **Fase 3:** Preparación de estructura del proyecto (directorios, archivos .env, docker-compose.yml)

---

## Troubleshooting

### Problema: El DNS no resuelve después de 1 hora

**Posibles causas:**

1. **Error en el registro DNS:** Verifica que el tipo sea **A** y no CNAME u otro
2. **IP incorrecta:** Confirma que la IP en el DNS coincide con `curl ifconfig.me` desde tu VPS
3. **Propagación lenta:** Algunos proveedores tardan más. Espera hasta 24 horas

**Solución:**

```bash
# Verificar IP pública del VPS
curl ifconfig.me

# Comparar con el DNS
nslookup n8n.tudominio.com
```

Si no coinciden, revisa la configuración DNS.

---

### Problema: Puerto 80 o 443 bloqueado desde fuera

**Síntoma:**

```powershell
Test-NetConnection -ComputerName TU_IP_VPS -Port 80
# TcpTestSucceeded : False
```

**Causas comunes en IONOS VPS:**

Este es uno de los problemas más frecuentes con IONOS porque tienen **dos firewalls**:
- UFW (en el servidor)
- Firewall del panel de IONOS (a nivel de red)

**Solución paso a paso:**

**1. Verificar UFW en el servidor:**
```bash
sudo ufw status
```

Si los puertos NO están permitidos:
```bash
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
sudo ufw reload
```

**2. Verificar firewall de IONOS (CRÍTICO):**

- Accede a https://my.ionos.es
- Ve a tu VPS → Configuración → Red → Firewall
- **Asegúrate de que las reglas para puerto 80 y 443 existen y están activas**
- Si no existen, créalas según indicado en el Paso 5.3 de esta guía

**3. Verificar desde el servidor que los puertos están abiertos:**
```bash
# Verificar que UFW está activo
sudo ufw status

# Intentar escuchar en el puerto (test rápido)
sudo nc -l 80
```

Cancela con Ctrl+C después de probar.

**4. Si nada funciona, usa la consola VNC de IONOS:**

Si accidentalmente te quedaste sin acceso SSH:
- Panel IONOS → Tu VPS → **Consola VNC**
- Accede directamente aunque el firewall esté bloqueando
- Corrige la configuración del firewall desde ahí

---

### Problema: Cloudflare con proxy naranja no valida SSL

**Síntoma:** Let's Encrypt no puede validar el dominio.

**Solución:**

1. En Cloudflare DNS, desactiva el proxy (nube gris, no naranja)
2. Espera 5 minutos
3. Vuelve a intentar

Una vez que Caddy haya generado el certificado SSL, puedes volver a activar el proxy de Cloudflare si lo deseas.

---

### Problema: DuckDNS no resuelve la IP

**Solución:**

1. Verifica que copiaste correctamente tu IP pública
2. Haz clic en "update ip" en el panel de DuckDNS
3. Espera 2-3 minutos
4. Vuelve a verificar con `nslookup`

---

### Problema: No tengo acceso al panel DNS de mi dominio

**Posibles causas:**

- Olvidaste las credenciales
- El dominio está registrado con otra cuenta
- El dominio expiró

**Solución:**

1. Recupera la contraseña del registrador
2. Verifica el estado del dominio (activo, expirado, etc.)
3. Si está expirado, renuévalo antes de continuar

---

### Problema: Perdí acceso SSH al servidor IONOS

**Síntoma:**

- No puedes conectarte por SSH
- Error: "Connection refused" o "Connection timed out"
- El firewall puede haber bloqueado el puerto 22

**Solución con la Consola VNC de IONOS:**

La consola VNC es una funcionalidad específica de IONOS que te permite acceder al servidor aunque SSH esté bloqueado.

**Pasos:**

1. **Acceder a la consola VNC:**
   - Ve a https://my.ionos.es
   - Selecciona tu VPS
   - Busca el botón **"Consola"** o **"VNC Console"**
   - Puede aparecer como un icono de pantalla 🖥️

2. **Se abrirá una ventana con acceso directo al servidor:**
   - Es como si estuvieras físicamente frente al servidor
   - No depende de la red ni del firewall

3. **Login en la consola:**
   - Usuario: `root` (o tu usuario)
   - Contraseña: la contraseña del servidor

4. **Arreglar el firewall:**
   ```bash
   # Permitir SSH de nuevo
   sudo ufw allow 22/tcp
   sudo ufw reload
   
   # Verificar
   sudo ufw status
   ```

5. **Cerrar la consola VNC** y volver a intentar SSH normal

**Notas sobre la consola VNC:**
- Es más lenta que SSH
- Úsala solo para emergencias o configuración inicial
- No depende de la configuración de red del VPS
- Siempre está disponible desde el panel de IONOS

---

### Problema: Mi proveedor no permite registros A en subdominios

**Solución alternativa:**

Algunos proveedores gratuitos tienen restricciones. Opciones:

1. **Migrar el dominio a Cloudflare** (gratis y sin restricciones)
2. **Usar DuckDNS** como alternativa temporal
3. **Cambiar de proveedor de dominio**

---

## Comandos de referencia rápida

**En el servidor VPS IONOS (vía SSH):**

```bash
# Obtener IP pública del VPS
curl ifconfig.me

# Verificar resolución DNS de n8n.sodire.es
nslookup n8n.sodire.es
dig n8n.sodire.es

# Verificar puertos abiertos en firewall UFW
sudo ufw status

# Abrir puertos necesarios
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp

# Verificar puertos escuchando
sudo ss -tlnp | grep -E ':(80|443)'

# Ver hostname del servidor
hostname
```

**Desde Windows (PowerShell):**

```powershell
# Verificar DNS de n8n.sodire.es
nslookup n8n.sodire.es

# Ping al dominio
ping n8n.sodire.es

# Probar conectividad de puerto
Test-NetConnection -ComputerName n8n.sodire.es -Port 80
Test-NetConnection -ComputerName n8n.sodire.es -Port 443
```

---

## Información importante para anotar

Antes de continuar a la Fase 3, asegúrate de tener anotado:

| Dato | Valor | Tu configuración |
|------|-------|------------------|
| **IP pública del VPS IONOS** | _________ | (obtener con `curl ifconfig.me`) |
| **Dominio completo para n8n** | **n8n.sodire.es** | ✅ Configurado |
| **Puerto SSH** | **22** | (estándar) |
| **Proveedor DNS** | **Cloudflare** | ✅ Configurado |
| **Fecha configuración DNS** | _________ | 16/03/2026 |
| **Hostname IONOS** | _________ | (ej: modest-napier.212-227-159-22.plesk.page) |
| **Usuario del VPS** | **root** | (normalmente) |
| **Firewall IONOS configurado** | ☐ Sí / ☐ No | Verificar en Panel IONOS |
| **UFW configurado** | ☐ Sí / ☐ No | `sudo ufw status` |

**Credenciales de acceso a guardar:**
- 🔑 Panel IONOS: https://my.ionos.es
- 🔑 Panel DNS del dominio
- 🔑 Contraseña root del VPS (guardada de forma segura)

Esta información la necesitarás en las siguientes fases.

---

## Próximos pasos

Una vez completada la Fase 2, procede con:

**Fase 3: Preparación de estructura del proyecto**
- Crear estructura de directorios
- Generar N8N_ENCRYPTION_KEY
- Crear archivo `.env` con todas las variables
- Preparar `docker-compose.yml`
- Configurar Caddyfile

---

## Notas adicionales

### Sobre DNS y propagación:

- **Tiempo de DNS:** La propagación DNS puede variar. Si tienes prisa, usa Cloudflare (propagación más rápida, 2-5 minutos).
- **Backup de configuración DNS:** Toma capturas de pantalla de tu configuración DNS por si necesitas replicarla.
- **Múltiples subdominios:** Puedes crear varios subdominios apuntando al mismo VPS si planeas instalar otros servicios.
- **IPv6:** Si tu VPS tiene IPv6, también puedes crear registros AAAA, pero no es obligatorio.
- **Wildcard DNS:** Algunos proveedores permiten registros comodín (`*.tudominio.com`), útil si planeas múltiples subdominios.

### Específico de IONOS VPS Linux:

- **Firewall de doble nivel:** Recuerda que IONOS tiene el firewall del panel web Y el UFW del servidor. Ambos deben estar configurados.
- **Consola VNC:** Siempre disponible desde el panel de IONOS, úsala si pierdes acceso SSH.
- **Snapshots:** IONOS permite crear snapshots (copias de seguridad instantáneas). Haz uno después de completar cada fase.
- **Hostname predefinido:** IONOS asigna hostnames como `modest-napier.212-227-159-22.plesk.page`. Puedes cambiarlo, pero no es necesario para n8n.
- **IP estática:** La IP de tu VPS IONOS es estática por defecto, no cambiará con reinicios.
- **Panel de control:** Accesible en https://my.ionos.es (España) o https://my.ionos.com (internacional).
- **Reinicio del VPS:** Puedes reiniciar el VPS desde el panel de IONOS sin perder la configuración.
- **Monitorización:** IONOS ofrece gráficas básicas de CPU, RAM y transferencia en el panel.

### Recomendaciones de seguridad para IONOS VPS:

- 🔒 Configura el firewall de IONOS para aceptar SSH solo desde tu IP si es posible
- 🔒 Considera cambiar el puerto SSH del 22 a otro personalizado
- 🔒 Usa claves SSH en lugar de contraseñas (configurable desde el panel IONOS)
- 🔒 Haz snapshots regulares (IONOS permite snapshots automáticos programados)

---

## Registro de ejecución

Usa esta tabla para documentar tu progreso en la Fase 2:

| Paso | Descripción | Fecha | Resultado | Notas |
|------|-------------|-------|-----------|-------|
| 1.1 | Obtener IP pública VPS IONOS | | | `curl ifconfig.me` |
| 1.2 | Verificar hostname IONOS | | | `hostname` |
| 2 | Decidir tipo de dominio | | | Propio / DuckDNS / IP |
| 3 | Configurar registro DNS tipo A | | | IP → Dominio |
| 4 | Verificar resolución DNS | | | `nslookup` |
| 5.1 | Configurar UFW en servidor | | | Puertos 22, 80, 443 |
| 5.2 | Configurar firewall panel IONOS | | | Panel web IONOS |
| 6 | Verificar acceso externo | | | `Test-NetConnection` |
| Extra | Crear snapshot en IONOS (recomendado) | | | Backup tras Fase 2 |

**Importante:** No olvides crear un snapshot en el panel de IONOS después de completar esta fase.

---

**Fin de la guía de Fase 2**

Documento creado: 16/03/2026  
Última actualización: 16/03/2026
