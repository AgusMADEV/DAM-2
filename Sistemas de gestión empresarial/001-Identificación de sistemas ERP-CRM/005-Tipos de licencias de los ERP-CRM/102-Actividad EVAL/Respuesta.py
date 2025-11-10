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