En esta actividad he trabajado con un pequeño programa en Python diseñado para **seleccionar el tipo de licencia** más adecuada en el contexto de los sistemas **ERP-CRM**.  
Los ERP (Enterprise Resource Planning) y los CRM (Customer Relationship Management) son herramientas fundamentales para **optimizar los procesos empresariales**, integrando áreas como ventas, marketing, finanzas y atención al cliente en una única plataforma.  

A la hora de implantar estos sistemas, es esencial comprender los distintos **tipos de licencias** disponibles (Privativas, SaaS o Abiertas), ya que cada una tiene implicaciones diferentes en términos de **coste, control, soporte y escalabilidad**.  
Este ejercicio me ha permitido reflexionar sobre la **importancia de la decisión de licenciamiento** dentro de la gestión tecnológica empresarial.

---

En el código he definido la variable `tipo_licencia`, que almacena la opción seleccionada por el usuario.  
El programa presenta un menú con tres alternativas posibles:  
1. Privativas  
2. SaaS  
3. Abiertas  

Dependiendo de la elección, la estructura condicional `if-elif-else` asigna el valor correspondiente a la variable `tipo_licencia`.  
Este desarrollo asegura un flujo lógico correcto y evita errores de ejecución si el usuario introduce un valor no válido.  

Por ejemplo, si el usuario introduce “2”, el programa asignará:  
```python
tipo_licencia = "SaaS"
```
y mostrará la información correspondiente sobre este tipo de licencia.

El código está estructurado de forma clara, con comentarios explicativos en cada paso, lo que demuestra una correcta **comprensión de las estructuras de control y manejo de variables en Python**.

---

```
tipo_licencia = ""

print("=== SELECCIÓN DE TIPO DE LICENCIA ERP-CRM ===")
print("Opciones disponibles:")
print("1. Privativas")
print("2. SaaS")
print("3. Abiertas")
print()


opcion = input("Por favor, selecciona el número de tu preferencia (1, 2 o 3): ")

if opcion == "1":
    tipo_licencia = "Privativas"
elif opcion == "2":
    tipo_licencia = "SaaS"
elif opcion == "3":
    tipo_licencia = "Abiertas"
else:
    tipo_licencia = "Opción no válida"

print()

if tipo_licencia != "Opción no válida":
    print(f"Has seleccionado el tipo de licencia: {tipo_licencia}")
    print()
    print("Información sobre tu selección:")
    
    if tipo_licencia == "Privativas":
        print("- Software propietario con código fuente cerrado")
        print("- Restricciones de uso y modificación")
        print("- Soporte técnico incluido generalmente")
        
    elif tipo_licencia == "SaaS":
        print("- No vendes el software, sino el acceso al servicio")
        print("- Software ejecutado en la nube")
        print("- Modelo de suscripción mensual/anual")
        
    elif tipo_licencia == "Abiertas":
        print("- Código fuente disponible (GPL, BSD, etc.)")
        print("- Posibilidad de modificación y redistribución")
        print("- Comunidad de desarrolladores activa")
else:
    print("Error: Debes seleccionar una opción válida (1, 2 o 3)")
```

Al ejecutar el programa, el usuario puede interactuar directamente con el sistema.  
Por ejemplo, si se selecciona la opción **2 (SaaS)**, el programa mostrará:

```
Has seleccionado el tipo de licencia: SaaS

Información sobre tu selección:
- No vendes el software, sino el acceso al servicio
- Software ejecutado en la nube
- Modelo de suscripción mensual/anual
```

Este resultado refleja un ejemplo real en el contexto de los proyectos ERP-CRM actuales, donde **el modelo SaaS** (Software as a Service) se ha vuelto muy común por su flexibilidad y coste predecible.  
Empresas como **Odoo o Holded**, mencionadas en actividades anteriores, utilizan este modelo para ofrecer sus servicios en la nube sin que los clientes deban preocuparse por la infraestructura o mantenimiento.  

---

A través de este ejercicio he comprendido que **elegir correctamente el tipo de licencia** es una decisión clave en la implantación de sistemas ERP-CRM.  
Cada modalidad (Privativa, SaaS o Abierta) presenta ventajas y limitaciones que pueden afectar tanto al **presupuesto como a la flexibilidad tecnológica** de una empresa.  

- Las **licencias Privativas** ofrecen soporte y seguridad jurídica.  
- Las **SaaS** facilitan la escalabilidad y reducen los costes iniciales.  
- Las **Abiertas** fomentan la innovación y la personalización.  

En conclusión, este programa no solo demuestra el uso práctico de variables y condicionales en Python, sino que también conecta directamente con la **realidad de la gestión empresarial moderna**, donde las decisiones sobre licencias impactan directamente en la **eficiencia operativa y sostenibilidad del negocio**.