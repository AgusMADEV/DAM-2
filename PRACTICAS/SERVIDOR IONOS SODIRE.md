SERVIDOR IONOS ***SODIRE***



**Cuenta:** sodire.info@gmail.com

**PASS:** Sodire21@



\----------------------------------------------------------



**SERVIDOR L:**



**\*\*IP\*\*** | 212.227.159.22

**PASS |** xckiW7w7oNjUDDCr



Dominio Cloudflare:



Sodire.es ---> DNS



\---------------------------------------------------------



**SERVIDOR L+ (n8n):**





**\*\*IP\*\*** | 212.227.255.246

**PASS |** QY8ON5vAwioNVj2



ssh d4htr95m-agustin@212.227.255.246

**\*\*USER\*\*** | d4htr95m-agustin

**PASS |** Agust1n2026@



Dominio IONOS: s0d1re.es



**MySQL:**



**\*\*USER\*\*** | agus

**PASS |** Agust1n2026@



\---------------------------------------------------------



**n8n** --> de momento en: http://212.227.255.246:5678/



**\*\*CORREO\*\*** | agustin.sodire@gmail.com

**PASS |** Agust1n2026@Agust1n2026@



\---------------------------------------------------------



**Comando backUp en servidor:** 



sudo tar -czf /home/d4htr95m-agustin/backup-n8n-post-setup-$(date +%F).tar.gz -C /var/lib/docker/volumes/root\_n8n\_data/\_data .



**Luego comprueba que se creó:**



ls -lh /home/d4htr95m-agustin/backup-n8n-post-setup-\*.tar.gz



**Y si quieres ver el contenido del backup:**



tar -tzf /home/d4htr95m-agustin/backup-n8n-post-setup-$(date +%F).tar.gz | head

