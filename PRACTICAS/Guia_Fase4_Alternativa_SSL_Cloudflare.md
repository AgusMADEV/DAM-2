# Guía Fase 4 (Alternativa): SSL con Cloudflare - SIN instalar nada en el VPS

**Proyecto:** Configuración de SSL sin instalar software en el VPS  
**Fase:** 4 Alternativa - SSL mediante Cloudflare  
**Dominio:** s0d1re.es / n8n.s0d1re.es  
**Método:** Cloudflare Proxy + SSL flexible  
**VPS IP:** 212.227.255.246  
**Fecha:** 23/03/2026

---

## 📋 Resumen rápido

**Objetivo:** Configurar HTTPS para n8n usando Cloudflare como proxy SSL, **sin instalar ningún software** en el VPS.

**Cómo funciona:**
```
Usuario → HTTPS → Cloudflare → HTTP → VPS (n8n en puerto 5678)
         ✅ SSL            ⚠️ Sin cifrar (pero en red interna de Cloudflare)
```

**Ventajas:**
- ✅ No instalas nada en el VPS
- ✅ SSL gratis de Cloudflare
- ✅ Protección DDoS incluida
- ✅ CDN global (carga más rápida)
- ✅ Firewall de aplicaciones web (WAF)
- ✅ Renovación automática de certificados

**Desventajas:**
- ⚠️ Debes mover el dominio a Cloudflare (cambiar nameservers en IONOS)
- ⚠️ Conexión VPS-Cloudflare va por HTTP (no cifrada)
- ⚠️ Dependes de un servicio externo
- ⚠️ Posible latencia adicional

**Tiempo estimado:** 30-40 minutos + propagación DNS (2-24h)

---

## Índice

1. [Requisitos previos](#requisitos-previos)
2. [Paso 1: Crear cuenta en Cloudflare](#paso-1-crear-cuenta-en-cloudflare)
3. [Paso 2: Añadir dominio a Cloudflare](#paso-2-añadir-dominio-a-cloudflare)
4. [Paso 3: Cambiar nameservers en IONOS](#paso-3-cambiar-nameservers-en-ionos)
5. [Paso 4: Configurar registros DNS](#paso-4-configurar-registros-dns)
6. [Paso 5: Configurar SSL en Cloudflare](#paso-5-configurar-ssl-en-cloudflare)
7. [Paso 6: Configurar n8n con el dominio](#paso-6-configurar-n8n-con-el-dominio)
8. [Paso 7: Verificar SSL](#paso-7-verificar-ssl)
9. [Paso 8: Optimizaciones de Cloudflare](#paso-8-optimizaciones-de-cloudflare)
10. [Comparativa: Cloudflare vs Caddy](#comparativa-cloudflare-vs-caddy)
11. [Troubleshooting](#troubleshooting)

---

## Requisitos previos

- ✅ Dominio s0d1re.es registrado en IONOS
- ✅ VPS activo (IP: 212.227.255.246)
- ✅ n8n funcionando en puerto 5678
- ✅ Email para crear cuenta Cloudflare (puedes usar: sodire.info@gmail.com)
- ✅ Acceso al panel de IONOS para cambiar nameservers

**⚠️ IMPORTANTE:**
- Este método requiere cambiar los nameservers de tu dominio
- Tu dominio dejará de usar los DNS de IONOS
- Toda la gestión DNS se hará desde Cloudflare

---

## Paso 1: Crear cuenta en Cloudflare

### 1.1. Registrarse en Cloudflare

1. Ve a: **https://dash.cloudflare.com/sign-up**
2. Introduce:
   - **Email:** sodire.info@gmail.com (o el que prefieras)
   - **Contraseña:** (crea una segura)
3. Haz clic en **"Create Account"**
4. Verifica tu email (revisa la bandeja de entrada)

### 1.2. Iniciar sesión

1. Ve a: **https://dash.cloudflare.com/login**
2. Introduce tus credenciales
3. Accede al panel principal

---

## Paso 2: Añadir dominio a Cloudflare

### 2.1. Añadir sitio

1. En el panel de Cloudflare, haz clic en **"Add a Site"** (Añadir un sitio)
2. Introduce tu dominio: **s0d1re.es**
3. Haz clic en **"Add site"**

### 2.2. Seleccionar plan

Cloudflare te preguntará qué plan quieres:

- **Free** (Gratis): ✅ Suficiente para n8n
- **Pro**: $20/mes (más funciones)
- **Business**: $200/mes
- **Enterprise**: Precio personalizado

**Selecciona:** **Free** (es suficiente)

Haz clic en **"Continue"**

### 2.3. Cloudflare escanea tus DNS

Cloudflare escaneará automáticamente los registros DNS existentes en IONOS.

**Esto puede tardar:** 30-60 segundos

**Resultado:** Verás una lista de registros DNS encontrados.

---

## Paso 3: Cambiar nameservers en IONOS

### 3.1. Obtener nameservers de Cloudflare

Después del escaneo, Cloudflare te mostrará dos nameservers:

**Ejemplo:**
```
eva.ns.cloudflare.com
fred.ns.cloudflare.com
```

**⚠️ Anota estos nameservers**, los necesitarás en IONOS.

### 3.2. Acceder al panel de IONOS

1. Ve a: **https://my.ionos.es**
2. Inicia sesión:
   - **Email:** sodire.info@gmail.com
   - **Contraseña:** Sodire21@

### 3.3. Localizar configuración de nameservers

1. En el panel de IONOS, ve a **"Dominios"**
2. Localiza **s0d1re.es**
3. Haz clic en el icono de configuración ⚙️ o en el dominio
4. Busca la opción:
   - **"Servidores de nombres"**
   - **"Nameservers"**
   - **"DNS"**
5. Haz clic en **"Cambiar servidores de nombres"** o similar

### 3.4. Cambiar a nameservers de Cloudflare

1. Selecciona: **"Usar otros servidores de nombres"** o **"Custom nameservers"**
2. Introduce los nameservers de Cloudflare:
   - **Nameserver 1:** eva.ns.cloudflare.com (o el que te dio Cloudflare)
   - **Nameserver 2:** fred.ns.cloudflare.com (o el que te dio Cloudflare)
3. Guarda los cambios

**⚠️ IMPORTANTE:**
- Este cambio puede tardar 2-24 horas en propagarse
- Durante este tiempo, tu dominio puede no funcionar correctamente
- Es normal, es parte del proceso

### 3.5. Confirmar en Cloudflare

1. Vuelve al panel de Cloudflare
2. Debería mostrarte un mensaje como:
   - "Waiting for nameserver change"
   - "Esperando cambio de nameservers"
3. Haz clic en **"Done, check nameservers"**

Cloudflare verificará periódicamente si los nameservers han cambiado.

**Recibirás un email cuando:**
- Los nameservers se hayan actualizado correctamente
- Tu sitio esté activo en Cloudflare

---

## Paso 4: Configurar registros DNS

### 4.1. Acceder a DNS en Cloudflare

Mientras esperas la propagación, puedes configurar los registros DNS:

1. En Cloudflare, selecciona tu dominio **s0d1re.es**
2. Ve a la pestaña **"DNS"** (en el menú lateral)
3. Haz clic en **"Records"** (Registros)

### 4.2. Revisar registros escaneados

Cloudflare habrá importado algunos registros automáticamente. Revisa si están estos:

| Tipo | Nombre | Contenido | Proxy | TTL |
|------|--------|-----------|-------|-----|
| A | @ (o s0d1re.es) | 212.227.255.246 | ✅ Proxied | Auto |
| A | www | 212.227.255.246 | ✅ Proxied | Auto |

### 4.3. Añadir/modificar registro para n8n

**Si no existe el registro para n8n:**

1. Haz clic en **"Add record"**
2. Rellena:
   - **Type:** A
   - **Name:** n8n
   - **IPv4 address:** 212.227.255.246
   - **Proxy status:** ✅ **Proxied** (naranja)
   - **TTL:** Auto
3. Haz clic en **"Save"**

**Si ya existe, verifica que esté correcto.**

### 4.4. Configurar proxy status

**⚠️ MUY IMPORTANTE:** El icono de la nube debe estar **NARANJA** (Proxied):

- 🟠 **Proxied (naranja):** El tráfico pasa por Cloudflare → Obtiene SSL
- ⚫ **DNS only (gris):** El tráfico va directamente al VPS → Sin SSL de Cloudflare

**Para activar el proxy:**
- Haz clic en el icono de la nube junto al registro
- Debe cambiar a naranja 🟠

### 4.5. Registros finales

Deberías tener algo así:

```
Tipo  | Nombre    | Contenido       | Proxy     | TTL
------|-----------|-----------------|-----------|-----
A     | @         | 212.227.255.246 | 🟠 Proxied | Auto
A     | www       | 212.227.255.246 | 🟠 Proxied | Auto
A     | n8n       | 212.227.255.246 | 🟠 Proxied | Auto
```

---

## Paso 5: Configurar SSL en Cloudflare

### 5.1. Acceder a configuración SSL

1. En el panel de Cloudflare, selecciona tu dominio
2. Ve a la pestaña **"SSL/TLS"**
3. Verás la configuración de SSL

### 5.2. Elegir modo SSL

Cloudflare ofrece varios modos SSL:

| Modo | Navegador → Cloudflare | Cloudflare → VPS | Seguridad |
|------|------------------------|------------------|-----------|
| **Off** | HTTP | HTTP | ❌ Ninguna |
| **Flexible** | HTTPS | HTTP | ⚠️ Media |
| **Full** | HTTPS | HTTPS (cualquier cert) | ✅ Buena |
| **Full (strict)** | HTTPS | HTTPS (cert válido) | ✅✅ Máxima |

**Para n8n sin instalar nada en el VPS:**

**Selecciona:** **Flexible** 🟡

- El navegador se conecta por HTTPS a Cloudflare ✅
- Cloudflare se conecta por HTTP al VPS ⚠️
- No necesitas instalar nada en el VPS ✅

**Nota:** Esta configuración es aceptable porque:
- La conexión vulnerable (HTTP) está dentro de la red de Cloudflare
- El usuario siempre ve HTTPS
- Es la única forma de tener SSL sin instalar nada

### 5.3. Configuraciones adicionales de SSL

#### 5.3.1. Always Use HTTPS

1. En la pestaña **"SSL/TLS"**, ve a **"Edge Certificates"**
2. Activa: **"Always Use HTTPS"**
   - Redirige automáticamente HTTP → HTTPS

#### 5.3.2. Automatic HTTPS Rewrites

1. En **"Edge Certificates"**
2. Activa: **"Automatic HTTPS Rewrites"**
   - Convierte enlaces HTTP internos a HTTPS

#### 5.3.3. Minimum TLS Version

1. En **"Edge Certificates"**
2. Configura: **TLS 1.2** (recomendado)
   - Balancea seguridad y compatibilidad

---

## Paso 6: Configurar n8n con el dominio

### 6.1. Conectarse al VPS

```bash
ssh d4htr95m-agustin@212.227.255.246
```

Contraseña: **QY8ON5vAwioNVj2**

### 6.2. Editar docker-compose.yml

```bash
nano docker-compose.yml
```

O si está en otra ubicación, usa la ruta correcta.

### 6.3. Añadir variables de entorno

Busca la sección `environment:` y añade:

```yaml
version: '3.8'

services:
  n8n:
    image: n8nio/n8n:latest
    container_name: n8n
    restart: unless-stopped
    ports:
      - "5678:5678"
    environment:
      - N8N_HOST=n8n.s0d1re.es
      - N8N_PORT=5678
      - N8N_PROTOCOL=https
      - WEBHOOK_URL=https://n8n.s0d1re.es/
      - GENERIC_TIMEZONE=Europe/Madrid
      - TZ=Europe/Madrid
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
```

**Variables importantes:**
- `N8N_HOST`: n8n.s0d1re.es
- `N8N_PROTOCOL`: **https** (importante)
- `WEBHOOK_URL`: https://n8n.s0d1re.es/

### 6.4. Guardar y reiniciar

```bash
# Guardar: Ctrl+O, Enter, Ctrl+X

# Reiniciar n8n
docker-compose down
docker-compose up -d
```

### 6.5. Verificar que n8n está corriendo

```bash
docker ps
```

---

## Paso 7: Verificar SSL

### 7.1. Esperar propagación

Antes de verificar, asegúrate de que:

1. **Nameservers propagados:** Habrás recibido email de Cloudflare
2. **DNS funcionando:** `nslookup n8n.s0d1re.es` devuelve una IP de Cloudflare

Para verificar propagación:

```bash
nslookup n8n.s0d1re.es
```

**Resultado esperado (una vez propagado):**
```
Name:   n8n.s0d1re.es
Address: 104.21.xxx.xxx  (IP de Cloudflare, NO tu VPS)
```

**Esto es correcto:** El DNS apunta a Cloudflare, que luego redirige a tu VPS.

### 7.2. Acceder por el navegador

Abre tu navegador y ve a:

```
https://n8n.s0d1re.es
```

**Deberías ver:**
- ✅ Candado verde
- ✅ Certificado SSL válido
- ✅ Interfaz de n8n

**Hacer clic en el candado:**
- Certificado emitido por: **Cloudflare Inc ECC CA-3**
- Válido para: n8n.s0d1re.es

### 7.3. Verificar redirección HTTP → HTTPS

Ve a:

```
http://n8n.s0d1re.es
```

Debería redirigirte automáticamente a:

```
https://n8n.s0d1re.es
```

### 7.4. Verificar desde línea de comandos

```powershell
curl -I https://n8n.s0d1re.es
```

**Resultado esperado:**
```
HTTP/2 200
date: ...
content-type: text/html
server: cloudflare
cf-ray: ...
```

---

## Paso 8: Optimizaciones de Cloudflare

### 8.1. Activar caché (opcional)

Para acelerar la carga:

1. Ve a **"Caching"** en Cloudflare
2. Configuración de nivel de caché: **Standard**
3. Browser Cache TTL: **4 hours** (o lo que prefieras)

**⚠️ Nota:** n8n es una aplicación dinámica, no necesita mucho caché.

### 8.2. Activar Brotli Compression

1. Ve a **"Speed"** → **"Optimization"**
2. Activa: **Brotli**
   - Comprime archivos para carga más rápida

### 8.3. Configurar Firewall (opcional)

1. Ve a **"Security"** → **"WAF"**
2. Security Level: **Medium** (recomendado)
3. Challenge passage: **30 minutes**

### 8.4. Page Rules (opcional)

Para optimizar específicamente n8n:

1. Ve a **"Rules"** → **"Page Rules"**
2. Crea regla para: `n8n.s0d1re.es/*`
3. Configuración:
   - Cache Level: **Bypass** (n8n es dinámico)
   - SSL: **Full** o **Flexible**
   - Always Use HTTPS: **On**

---

## Comparativa: Cloudflare vs Caddy

### Método Cloudflare (este método)

**✅ Ventajas:**
- No instalas nada en el VPS
- SSL gratis de Cloudflare
- Protección DDoS
- CDN global
- Firewall de aplicaciones web
- Fácil gestión desde panel web

**❌ Desventajas:**
- Conexión VPS-Cloudflare sin cifrar (HTTP)
- Dependes de servicio externo
- Necesitas cambiar nameservers
- Posible latencia adicional
- Datos pasan por servidores de Cloudflare

### Método Caddy (Guía Fase 4 principal)

**✅ Ventajas:**
- Conexión completamente cifrada (end-to-end)
- Sin dependencias externas
- Más control total
- Mejor privacidad (no pasa por terceros)
- Certificados propios de Let's Encrypt

**❌ Desventajas:**
- Requiere instalar Caddy (pero es muy simple)
- Gestión desde línea de comandos
- No incluye protección DDoS
- No incluye CDN

---

## ✅ Checklist de verificación

**Cloudflare:**
- [ ] Cuenta creada en Cloudflare
- [ ] Dominio añadido a Cloudflare
- [ ] Nameservers cambiados en IONOS
- [ ] Email de confirmación recibido
- [ ] Registros DNS configurados (A para @, www, n8n)
- [ ] Proxy status: 🟠 naranja (Proxied)
- [ ] SSL mode: Flexible

**n8n:**
- [ ] docker-compose.yml actualizado
- [ ] N8N_HOST configurado
- [ ] N8N_PROTOCOL=https configurado
- [ ] WEBHOOK_URL configurado
- [ ] n8n reiniciado

**Verificación:**
- [ ] https://n8n.s0d1re.es carga correctamente
- [ ] Candado verde en navegador
- [ ] HTTP redirige a HTTPS
- [ ] Inicio de sesión funciona
- [ ] Webhooks usan HTTPS

---

## Troubleshooting

### ❌ Problema: "ERR_TOO_MANY_REDIRECTS"

**Síntoma:** Loop de redirecciones infinitas

**Causa:** Configuración SSL incorrecta

**Solución:**

1. Ve a Cloudflare → **"SSL/TLS"**
2. Cambia el modo SSL a: **Flexible**
3. En n8n, asegúrate de que `N8N_PROTOCOL=https`
4. Espera 2-3 minutos y recarga

### ❌ Problema: Cloudflare no detecta el cambio de nameservers

**Soluciones:**

1. **Verifica los nameservers desde tu ordenador:**
   ```powershell
   nslookup -type=NS s0d1re.es
   ```
   Deberías ver los nameservers de Cloudflare

2. **Limpia caché DNS:**
   ```powershell
   ipconfig /flushdns
   ```

3. **Espera más tiempo:** Puede tardar hasta 24 horas

4. **Verifica en IONOS:** Asegúrate de que guardaste los cambios

### ❌ Problema: "This site can't provide a secure connection"

**Causa:** SSL aún no activado en Cloudflare

**Solución:**

1. Ve a **"SSL/TLS"** en Cloudflare
2. Verifica que el modo sea **Flexible**
3. Espera 2-3 minutos (Cloudflare genera el certificado)
4. Limpia caché del navegador

### ❌ Problema: El sitio carga pero sin SSL

**Solución:**

1. Verifica que el proxy esté activado (icono naranja 🟠)
2. Ve a **"SSL/TLS"** → **"Edge Certificates"**
3. Activa **"Always Use HTTPS"**
4. Espera 2-3 minutos

---

## 🎯 ¿Cuál es mejor para ti?

### Usa **Cloudflare** (este método) si:
- ✅ No quieres instalar nada en el VPS
- ✅ Quieres protección DDoS
- ✅ Valoras la simplicidad de gestión web
- ✅ No te importa que el tráfico pase por Cloudflare

### Usa **Caddy** (Guía Fase 4 principal) si:
- ✅ Quieres cifrado end-to-end completo
- ✅ Prefieres control total
- ✅ No te importa instalar un programa simple
- ✅ Valoras la privacidad (sin terceros)

---

## 📝 Comandos rápidos de referencia

```bash
# Verificar DNS
nslookup n8n.s0d1re.es

# Ver nameservers actuales
nslookup -type=NS s0d1re.es

# Verificar n8n
docker ps
docker logs n8n

# Reiniciar n8n
docker-compose restart

# Ver configuración n8n
cat docker-compose.yml
```

---

**Guía creada:** 23/03/2026  
**Última actualización:** 23/03/2026  
**Versión:** 1.0
