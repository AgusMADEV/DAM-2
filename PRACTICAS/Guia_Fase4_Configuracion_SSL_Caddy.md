# Guía Fase 4: Configuración de SSL con Caddy para s0d1re.es

**Proyecto:** Configuración de SSL automático para n8n  
**Fase:** 4 - Proxy inverso y certificados SSL  
**Dominio:** s0d1re.es / n8n.s0d1re.es  
**Proxy:** Caddy (con SSL automático)  
**VPS IP:** 212.227.255.246  
**Fecha:** 23/03/2026

---

## 📋 Resumen rápido

**Objetivo:** Configurar Caddy como proxy inverso con certificados SSL automáticos para acceder a n8n de forma segura mediante HTTPS.

**Lo que vas a lograr:**
- ✅ Caddy instalado como proxy inverso
- ✅ Certificados SSL automáticos de Let's Encrypt
- ✅ Acceso seguro a n8n: https://n8n.s0d1re.es
- ✅ Renovación automática de certificados
- ✅ Redirección HTTP → HTTPS

**Antes de empezar, asegúrate de:**
- ✅ DNS propagado (s0d1re.es y n8n.s0d1re.es apuntan a 212.227.255.246)
- ✅ Puertos 80 y 443 abiertos en firewall
- ✅ n8n funcionando en http://212.227.255.246:5678

**Tiempo estimado:** 30-45 minutos

---

## Índice

1. [Requisitos previos](#requisitos-previos)
2. [Paso 1: Verificar DNS propagado](#paso-1-verificar-dns-propagado)
3. [Paso 2: Instalar Caddy](#paso-2-instalar-caddy)
4. [Paso 3: Configurar Caddy para n8n](#paso-3-configurar-caddy-para-n8n)
5. [Paso 4: Configurar n8n con el dominio](#paso-4-configurar-n8n-con-el-dominio)
6. [Paso 5: Aplicar configuración](#paso-5-aplicar-configuración)
7. [Paso 6: Verificar certificados SSL](#paso-6-verificar-certificados-ssl)
8. [Paso 7: Cerrar acceso directo a puerto 5678](#paso-7-cerrar-acceso-directo-a-puerto-5678)
9. [Paso 8: (Opcional) Configurar dominio principal](#paso-8-opcional-configurar-dominio-principal)
10. [Verificación final](#verificación-final)
11. [Mantenimiento y renovación](#mantenimiento-y-renovación)
12. [Troubleshooting](#troubleshooting)

---

## Requisitos previos

Antes de comenzar, verifica que has completado:

- ✅ **Fase 3:** DNS configurado y propagado
- ✅ DNS de s0d1re.es apunta a 212.227.255.246
- ✅ DNS de n8n.s0d1re.es apunta a 212.227.255.246
- ✅ Puertos 80 y 443 abiertos en firewall IONOS
- ✅ Puertos 80 y 443 abiertos en UFW
- ✅ n8n funcionando en http://212.227.255.246:5678
- ✅ Acceso SSH al VPS

---

## Paso 1: Verificar DNS propagado

### 1.1. Conectarse al VPS

```bash
ssh d4htr95m-agustin@212.227.255.246
```

Contraseña: **QY8ON5vAwioNVj2**

### 1.2. Verificar DNS desde el VPS

```bash
# Verificar n8n.s0d1re.es
nslookup n8n.s0d1re.es
```

**Resultado esperado:**
```
Server:         127.0.0.53
Address:        127.0.0.53#53

Non-authoritative answer:
Name:   n8n.s0d1re.es
Address: 212.227.255.246
```

También verifica con `dig`:

```bash
dig n8n.s0d1re.es +short
```

**Resultado esperado:**
```
212.227.255.246
```

### 1.3. Verificar dominio principal

```bash
dig s0d1re.es +short
```

**⚠️ IMPORTANTE:** Si los comandos anteriores NO devuelven tu IP (212.227.255.246), **DETENTE AQUÍ**.

Los certificados SSL necesitan que el DNS esté correctamente propagado. Espera a que se propague antes de continuar.

---

## Paso 2: Instalar Caddy

### 2.1. ¿Por qué Caddy?

**Ventajas de Caddy sobre Nginx:**
- ✅ SSL automático con Let's Encrypt (sin configuración)
- ✅ Renovación automática de certificados
- ✅ Configuración más simple y legible
- ✅ HTTP/2 y HTTP/3 por defecto
- ✅ Sin archivos complejos de configuración

### 2.2. Instalar dependencias

```bash
sudo apt update
sudo apt install -y debian-keyring debian-archive-keyring apt-transport-https curl
```

### 2.3. Añadir el repositorio oficial de Caddy

```bash
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/gpg.key' | sudo gpg --dearmor -o /usr/share/keyrings/caddy-stable-archive-keyring.gpg
```

```bash
curl -1sLf 'https://dl.cloudsmith.io/public/caddy/stable/debian.deb.txt' | sudo tee /etc/apt/sources.list.d/caddy-stable.list
```

### 2.4. Actualizar e instalar Caddy

```bash
sudo apt update
sudo apt install caddy
```

**Tiempo estimado:** 1-2 minutos

### 2.5. Verificar instalación

```bash
caddy version
```

**Resultado esperado:**
```
v2.7.6 h1:w0NymbG2m9PcvKWsrXO6EEkY9Ru4FJK8uQbYcev1p3A=
```

(La versión puede variar)

### 2.6. Verificar que Caddy está corriendo

```bash
sudo systemctl status caddy
```

**Resultado esperado:**
```
● caddy.service - Caddy
     Loaded: loaded (/lib/systemd/system/caddy.service; enabled; vendor preset: enabled)
     Active: active (running) since...
```

Presiona `q` para salir.

### 2.7. Verificar que Caddy está escuchando en puerto 80

```bash
sudo ss -tlnp | grep :80
```

**Resultado esperado:**
```
LISTEN 0      4096         *:80        *:*    users:(("caddy",pid=1234,fd=5))
```

---

## Paso 3: Configurar Caddy para n8n

### 3.1. Hacer backup de la configuración por defecto

```bash
sudo cp /etc/caddy/Caddyfile /etc/caddy/Caddyfile.backup
```

### 3.2. Editar el archivo de configuración de Caddy

```bash
sudo nano /etc/caddy/Caddyfile
```

### 3.3. Borrar todo el contenido y reemplazarlo

Presiona `Ctrl+K` varias veces para borrar todas las líneas.

Luego, copia y pega esta configuración:

```
# Configuración para n8n.s0d1re.es
n8n.s0d1re.es {
    # Proxy inverso a n8n
    reverse_proxy localhost:5678 {
        # Headers para WebSocket (necesario para n8n)
        header_up X-Real-IP {remote_host}
        header_up X-Forwarded-For {remote_host}
        header_up X-Forwarded-Proto {scheme}
        header_up X-Forwarded-Host {host}
    }

    # Logs
    log {
        output file /var/log/caddy/n8n-access.log
        format json
    }

    # Compresión automática
    encode gzip

    # Headers de seguridad
    header {
        # Evitar clickjacking
        X-Frame-Options "SAMEORIGIN"
        # Evitar MIME sniffing
        X-Content-Type-Options "nosniff"
        # Política de referrer
        Referrer-Policy "strict-origin-when-cross-origin"
        # Eliminar header Server
        -Server
    }
}

# Redirección de dominio principal a subdominio n8n (opcional)
s0d1re.es {
    redir https://n8n.s0d1re.es{uri} permanent
}

www.s0d1re.es {
    redir https://n8n.s0d1re.es{uri} permanent
}
```

### 3.4. Guardar el archivo

1. Presiona `Ctrl+O` (guardar)
2. Presiona `Enter` (confirmar nombre)
3. Presiona `Ctrl+X` (salir)

### 3.5. Explicación de la configuración

**n8n.s0d1re.es:**
- Caddy obtiene automáticamente el certificado SSL de Let's Encrypt
- Redirige todo el tráfico a `http://localhost:5678` (n8n)
- Añade headers necesarios para WebSocket (usado por n8n)
- Aplica compresión gzip
- Añade headers de seguridad

**s0d1re.es y www.s0d1re.es:**
- Redirige a `https://n8n.s0d1re.es`
- Útil para que los usuarios accedan directamente

### 3.6. Verificar sintaxis de la configuración

```bash
sudo caddy validate --config /etc/caddy/Caddyfile
```

**Resultado esperado:**
```
Valid configuration
```

**Si hay errores:**
- Revisa que hayas copiado correctamente la configuración
- Verifica que no haya espacios o tabulaciones incorrectas
- Vuelve a editar con `sudo nano /etc/caddy/Caddyfile`

---

## Paso 4: Configurar n8n con el dominio

### 4.1. Localizar el archivo docker-compose.yml de n8n

```bash
cd ~
ls -la
```

Busca el archivo `docker-compose.yml` o navega a la carpeta donde instalaste n8n.

**Posibles ubicaciones:**
- `/root/docker-compose.yml`
- `/home/d4htr95m-agustin/docker-compose.yml`
- `/opt/n8n/docker-compose.yml`

Si no lo encuentras, busca:

```bash
sudo find / -name "docker-compose.yml" 2>/dev/null | grep -v snap
```

### 4.2. Editar el archivo docker-compose.yml

```bash
sudo nano docker-compose.yml
```

O si está en otra ubicación:

```bash
sudo nano /ruta/al/docker-compose.yml
```

### 4.3. Añadir variables de entorno para el dominio

Busca la sección de `environment:` de n8n y añade estas líneas:

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
      # ... otras variables que ya tenías
    volumes:
      - n8n_data:/home/node/.n8n

volumes:
  n8n_data:
```

**Variables importantes:**
- `N8N_HOST`: Tu dominio (n8n.s0d1re.es)
- `N8N_PROTOCOL`: https (para usar SSL)
- `WEBHOOK_URL`: URL completa para webhooks

### 4.4. Guardar y salir

1. `Ctrl+O` → Enter (guardar)
2. `Ctrl+X` (salir)

### 4.5. Reiniciar n8n

```bash
docker-compose down
docker-compose up -d
```

**Verificar que n8n está corriendo:**

```bash
docker ps
```

**Resultado esperado:**
```
CONTAINER ID   IMAGE              STATUS          PORTS                    NAMES
abc123def456   n8nio/n8n:latest   Up 10 seconds   0.0.0.0:5678->5678/tcp   n8n
```

### 4.6. Ver logs de n8n (opcional)

```bash
docker logs n8n -f
```

Presiona `Ctrl+C` para salir.

---

## Paso 5: Aplicar configuración

### 5.1. Crear directorio para logs de Caddy

```bash
sudo mkdir -p /var/log/caddy
sudo chown caddy:caddy /var/log/caddy
```

### 5.2. Recargar configuración de Caddy

```bash
sudo systemctl reload caddy
```

**Alternativamente:**

```bash
sudo caddy reload --config /etc/caddy/Caddyfile
```

### 5.3. Verificar estado de Caddy

```bash
sudo systemctl status caddy
```

**Resultado esperado:**
```
● caddy.service - Caddy
     Loaded: loaded
     Active: active (running)
```

### 5.4. Ver logs de Caddy en tiempo real

```bash
sudo journalctl -u caddy -f
```

**Deberías ver:**
- Caddy obteniendo certificados SSL de Let's Encrypt
- Mensajes como: "certificate obtained successfully"
- Sin errores de conexión

Presiona `Ctrl+C` para salir.

---

## Paso 6: Verificar certificados SSL

### 6.1. Verificar desde el navegador

Abre tu navegador y ve a:

```
https://n8n.s0d1re.es
```

**Deberías ver:**
- ✅ Candado verde en la barra de direcciones
- ✅ La interfaz de n8n cargando correctamente
- ✅ Sin advertencias de seguridad

**Hacer clic en el candado:**
- Debería decir "Conexión segura"
- Certificado emitido por: Let's Encrypt
- Válido para: n8n.s0d1re.es

### 6.2. Verificar certificado desde línea de comandos

Desde tu ordenador local (PowerShell):

```powershell
curl -I https://n8n.s0d1re.es
```

**Resultado esperado:**
```
HTTP/2 200
server: Caddy
...
```

### 6.3. Verificar redirección HTTP → HTTPS

Ve a:

```
http://n8n.s0d1re.es
```

Debería redirigirte automáticamente a:

```
https://n8n.s0d1re.es
```

### 6.4. Comprobar certificado SSL online

Ve a: **https://www.ssllabs.com/ssltest/**

1. Introduce: `n8n.s0d1re.es`
2. Haz clic en "Submit"
3. Espera el análisis (2-3 minutos)

**Resultado esperado:**
- Calificación: A o A+
- Certificado válido
- Protocolos modernos habilitados

### 6.5. Ver detalles del certificado en el VPS

```bash
sudo ls -la /var/lib/caddy/.local/share/caddy/certificates/acme-v02.api.letsencrypt.org-directory/
```

**Deberías ver:**
- Carpetas con tus dominios (n8n.s0d1re.es, s0d1re.es)
- Archivos .crt (certificados)
- Archivos .key (claves privadas)

---

## Paso 7: Cerrar acceso directo a puerto 5678

### 7.1. ¿Por qué cerrar el puerto 5678?

Ahora que n8n es accesible vía HTTPS en https://n8n.s0d1re.es, **no necesitas** el acceso directo en el puerto 5678.

**Ventajas de cerrarlo:**
- ✅ Más seguro (un solo punto de entrada)
- ✅ Todo el tráfico pasa por SSL
- ✅ Evita accesos no autorizados

### 7.2. Cerrar puerto 5678 en UFW

```bash
sudo ufw status numbered
```

Busca la regla del puerto 5678. Verás algo como:

```
[4] 5678/tcp                   ALLOW IN    Anywhere
```

Elimina la regla (reemplaza el número según tu configuración):

```bash
sudo ufw delete 4
```

Confirma con `y`.

**Verificar:**

```bash
sudo ufw status
```

El puerto 5678 ya no debería aparecer.

### 7.3. Cerrar puerto 5678 en firewall IONOS

1. Ve al panel de IONOS: https://my.ionos.es
2. Accede al VPS
3. Firewall
4. Localiza la regla del puerto 5678
5. Elimínala o desactívala

### 7.4. (Opcional) Limitar acceso del puerto 5678 solo a localhost

**Alternativa:** En lugar de cerrar el puerto, configura n8n para escuchar solo en localhost.

Edita `docker-compose.yml`:

```bash
sudo nano docker-compose.yml
```

Cambia:

```yaml
ports:
  - "5678:5678"
```

Por:

```yaml
ports:
  - "127.0.0.1:5678:5678"
```

Esto hace que el puerto 5678 solo sea accesible desde localhost (donde está Caddy).

**Reinicia n8n:**

```bash
docker-compose down
docker-compose up -d
```

### 7.5. Verificar que el puerto está cerrado externamente

Desde tu ordenador local, intenta acceder:

```
http://212.227.255.246:5678
```

**Debería:**
- No cargar (timeout)
- O mostrar "Connection refused"

Mientras que:

```
https://n8n.s0d1re.es
```

**Sigue funcionando correctamente.**

---

## Paso 8: (Opcional) Configurar dominio principal

Si quieres que `https://s0d1re.es` muestre algo en lugar de solo redireccionar a n8n:

### 8.1. Opción A: Página de inicio simple

Edita el Caddyfile:

```bash
sudo nano /etc/caddy/Caddyfile
```

Reemplaza la sección de `s0d1re.es`:

```
s0d1re.es {
    root * /var/www/s0d1re.es
    file_server

    log {
        output file /var/log/caddy/s0d1re-access.log
    }
}
```

Crea la página:

```bash
sudo mkdir -p /var/www/s0d1re.es
sudo nano /var/www/s0d1re.es/index.html
```

Añade contenido HTML:

```html
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>s0d1re.es</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            display: flex;
            justify-content: center;
            align-items: center;
            height: 100vh;
            margin: 0;
            background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
            color: white;
        }
        .container {
            text-align: center;
        }
        h1 { font-size: 3em; margin-bottom: 0.5em; }
        a {
            color: white;
            text-decoration: none;
            border: 2px solid white;
            padding: 10px 30px;
            border-radius: 5px;
            display: inline-block;
            margin-top: 20px;
            transition: all 0.3s;
        }
        a:hover {
            background: white;
            color: #667eea;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>s0d1re.es</h1>
        <p>Bienvenido a mi servidor</p>
        <a href="https://n8n.s0d1re.es">Acceder a n8n</a>
    </div>
</body>
</html>
```

Guarda y recarga Caddy:

```bash
sudo systemctl reload caddy
```

Ahora `https://s0d1re.es` mostrará esta página.

### 8.2. Opción B: Mantener redirección

Si prefieres que `s0d1re.es` redirija directamente a `n8n.s0d1re.es`, deja la configuración como está (ya configurada en Paso 3.3).

---

## Verificación final

### ✅ Checklist completo

**Instalación:**
- [ ] Caddy instalado correctamente
- [ ] Configuración de Caddy creada
- [ ] n8n configurado con N8N_HOST y N8N_PROTOCOL

**Certificados SSL:**
- [ ] https://n8n.s0d1re.es carga correctamente
- [ ] Candado verde en el navegador
- [ ] Certificado emitido por Let's Encrypt
- [ ] Sin advertencias de seguridad
- [ ] Redirección HTTP → HTTPS funciona

**Seguridad:**
- [ ] Puerto 5678 cerrado externamente
- [ ] Solo puertos 22, 80, 443 abiertos
- [ ] http://212.227.255.246:5678 no es accesible
- [ ] https://n8n.s0d1re.es funciona perfectamente

**Funcionalidad:**
- [ ] Puedes iniciar sesión en n8n
- [ ] n8n funciona correctamente con el dominio
- [ ] Webhooks usan https://n8n.s0d1re.es

**Dominios adicionales:**
- [ ] https://s0d1re.es funciona (redirección o página)
- [ ] https://www.s0d1re.es funciona (redirección)

---

## Mantenimiento y renovación

### Renovación automática de certificados

**La buena noticia:** Caddy renueva automáticamente los certificados SSL.

- Certificados de Let's Encrypt duran **90 días**
- Caddy los renueva automáticamente **30 días antes** de expirar
- **No necesitas hacer nada manualmente**

### Verificar cuándo expira el certificado

```bash
echo | openssl s_client -servername n8n.s0d1re.es -connect n8n.s0d1re.es:443 2>/dev/null | openssl x509 -noout -dates
```

**Resultado:**
```
notBefore=Mar 23 10:30:00 2026 GMT
notAfter=Jun 21 10:30:00 2026 GMT
```

### Ver logs de renovación

```bash
sudo journalctl -u caddy | grep -i "certificate"
```

### Forzar renovación manual (si es necesario)

```bash
sudo caddy reload --config /etc/caddy/Caddyfile
```

### Backup de certificados (recomendado)

```bash
sudo tar -czf ~/caddy-certificates-backup-$(date +%F).tar.gz /var/lib/caddy/.local/share/caddy/certificates/
```

---

## Troubleshooting

### ❌ Problema: https://n8n.s0d1re.es no carga

**Síntomas:** Timeout, "No se puede acceder al sitio"

**Soluciones:**

1. **Verificar que Caddy está corriendo:**
   ```bash
   sudo systemctl status caddy
   ```

2. **Verificar logs de Caddy:**
   ```bash
   sudo journalctl -u caddy -n 50
   ```

3. **Verificar que los puertos están abiertos:**
   ```bash
   sudo ss -tlnp | grep -E ':(80|443)'
   ```

4. **Probar con curl desde el VPS:**
   ```bash
   curl -I http://localhost:80
   curl -I https://n8n.s0d1re.es
   ```

5. **Verificar DNS:**
   ```bash
   dig n8n.s0d1re.es +short
   ```

### ❌ Problema: Error "unable to get certificate"

**Síntomas:** Caddy no puede obtener el certificado SSL

**Causas comunes:**

1. **DNS no propagado:** Espera más tiempo
2. **Puerto 80 bloqueado:** Let's Encrypt necesita puerto 80 para validar
3. **Firewall bloqueando:** Verifica firewall IONOS y UFW

**Soluciones:**

1. **Verificar que el puerto 80 está abierto:**
   ```bash
   sudo ufw status | grep 80
   sudo ss -tlnp | grep :80
   ```

2. **Verificar DNS desde múltiples ubicaciones:**
   - https://dnschecker.org

3. **Ver logs detallados de Caddy:**
   ```bash
   sudo journalctl -u caddy -f
   ```

4. **Probar obtener certificado manualmente:**
   ```bash
   sudo caddy validate --config /etc/caddy/Caddyfile
   sudo systemctl restart caddy
   sudo journalctl -u caddy -n 100
   ```

### ❌ Problema: Certificado SSL funciona pero n8n no carga

**Síntomas:** https funciona pero muestra error 502 Bad Gateway

**Soluciones:**

1. **Verificar que n8n está corriendo:**
   ```bash
   docker ps
   ```

2. **Verificar logs de n8n:**
   ```bash
   docker logs n8n --tail 50
   ```

3. **Reiniciar n8n:**
   ```bash
   docker-compose restart
   ```

4. **Verificar que n8n escucha en puerto 5678:**
   ```bash
   sudo ss -tlnp | grep 5678
   ```

5. **Probar acceso directo desde VPS:**
   ```bash
   curl http://localhost:5678
   ```

### ❌ Problema: Advertencia de seguridad en el navegador

**Síntomas:** "Tu conexión no es privada" o "Certificado no válido"

**Causas:**

1. Certificado aún no obtenido
2. Dominio no coincide con el certificado
3. Certificado expirado

**Soluciones:**

1. **Esperar 2-3 minutos** después de recargar Caddy
2. **Verificar el certificado:**
   ```bash
   sudo journalctl -u caddy | grep -i certificate
   ```
3. **Forzar obtención:**
   ```bash
   sudo systemctl restart caddy
   ```

### ❌ Problema: n8n funciona pero webhooks no

**Síntomas:** Automatizaciones activadas por webhook no funcionan

**Causa:** Variable WEBHOOK_URL incorrecta

**Solución:**

Edita `docker-compose.yml`:

```bash
sudo nano docker-compose.yml
```

Asegúrate de tener:

```yaml
environment:
  - WEBHOOK_URL=https://n8n.s0d1re.es/
```

Reinicia:

```bash
docker-compose down
docker-compose up -d
```

### ❌ Problema: "Certificate is about to expire" pero no se renueva

**Solución:**

1. **Verificar que Caddy puede acceder a Let's Encrypt:**
   ```bash
   curl -I https://acme-v02.api.letsencrypt.org
   ```

2. **Reiniciar Caddy:**
   ```bash
   sudo systemctl restart caddy
   ```

3. **Ver si hay errores:**
   ```bash
   sudo journalctl -u caddy | grep -i error
   ```

---

## 🎯 Próximos pasos

Una vez completada esta fase, tu instalación de n8n está **completamente funcional** con:

- ✅ Dominio personalizado
- ✅ Certificados SSL automáticos
- ✅ Conexión segura HTTPS
- ✅ Renovación automática

**Recomendaciones para Fase 5:**

1. **Seguridad avanzada:**
   - Configurar autenticación de dos factores en n8n
   - Configurar fail2ban
   - Configurar backups automáticos

2. **Optimización:**
   - Configurar base de datos PostgreSQL (si usas SQLite)
   - Configurar caché
   - Optimizar rendimiento

3. **Monitorización:**
   - Configurar alertas de expirción de certificados
   - Monitorizar uso de recursos
   - Logs centralizados

---

## 📚 Recursos adicionales

**Documentación:**
- Caddy: https://caddyserver.com/docs/
- Let's Encrypt: https://letsencrypt.org/docs/
- n8n HTTPS: https://docs.n8n.io/hosting/configuration/

**Herramientas útiles:**
- SSL Labs: https://www.ssllabs.com/ssltest/
- DNS Checker: https://dnschecker.org
- Caddy GUI: https://caddyserver.com/v2/docs/

---

## 📝 Comandos rápidos de referencia

```bash
# Ver estado de Caddy
sudo systemctl status caddy

# Recargar configuración de Caddy
sudo systemctl reload caddy

# Reiniciar Caddy
sudo systemctl restart caddy

# Ver logs de Caddy
sudo journalctl -u caddy -f

# Validar configuración
sudo caddy validate --config /etc/caddy/Caddyfile

# Ver certificados
sudo ls -la /var/lib/caddy/.local/share/caddy/certificates/

# Verificar n8n
docker ps
docker logs n8n

# Reiniciar n8n
docker-compose restart

# Ver puertos abiertos
sudo ss -tlnp | grep -E ':(80|443|5678)'
```

---

**Guía creada:** 23/03/2026  
**Última actualización:** 23/03/2026  
**Versión:** 1.0
