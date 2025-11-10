En esta actividad he analizado las **tecnologías principales utilizadas en los sistemas ERP-CRM** para la gestión de bases de datos y la comunicación con el backend.  
Los sistemas ERP-CRM requieren una infraestructura sólida que permita manejar **grandes volúmenes de información de clientes, productos, ventas y operaciones** de manera eficiente.  

A partir del contenido trabajado en clase, he identificado tres grandes grupos tecnológicos: **SQL, NoSQL y ficheros planos**, además de los mecanismos que permiten **la separación de la capa de conexión** y el uso de **ORM (Object-Relational Mapping)** para facilitar el desarrollo.  
Comprender estas tecnologías es fundamental para poder diseñar sistemas empresariales escalables y mantenibles.

---

### 🔹 Tecnologías principales de bases de datos  
1. **SQL (Relacionales):** Usadas en la mayoría de los ERP empresariales. Ejemplos: *MySQL, PostgreSQL, Oracle Database y Microsoft SQL Server*. Estas bases se caracterizan por su estructura tabular, uso del lenguaje SQL y cumplimiento de las propiedades ACID.  
2. **NoSQL (No estructuradas):** Ideales para datos masivos y distribuidos, como *MongoDB* o *Redis*, que permiten gran flexibilidad en el formato de los datos.  
3. **Ficheros planos/personalizados:** Utilizados en proyectos pequeños o en etapas iniciales del desarrollo, con formatos como *CSV, XML o JSON*.  

### 🔹 Separación de la conexión al backend  
Separar la conexión de la base de datos de la lógica de negocio es una **buena práctica de desarrollo**, ya que:  
- Mantiene el código limpio y modular.  
- Permite cambiar de base de datos sin alterar la estructura principal.  
- Mejora la escalabilidad del sistema y la reutilización del código.  

Por ejemplo, en un proyecto ERP, la capa de conexión podría estar contenida en un archivo `db_connection.py`, mientras que la lógica del negocio estaría en módulos separados que utilizan esa conexión.

### 🔹 ORM (Object-Relational Mapping)  
Los sistemas ERP modernos suelen estar desarrollados en lenguajes orientados a objetos, por lo que el uso de un **ORM** facilita la conexión con bases de datos relacionales.  
El ORM convierte los **objetos del código (por ejemplo, “Cliente” o “Factura”) en registros de base de datos**, lo que ahorra tiempo y evita escribir consultas SQL complejas.  

Ejemplos de ORMs comunes:  
- **Django ORM (Python)**  
- **Hibernate (Java)**  
- **Entity Framework (.NET)**  
- **ActiveRecord (Ruby)**  

Estos sistemas permiten escribir código más legible y menos dependiente de un motor de base de datos específico.

---

Para entender mejor la ventaja del ORM, veamos cómo se implementaría la gestión de clientes en un sistema ERP-CRM **sin ORM** y **con ORM**:

### 🔸 **SIN ORM** (Conexión directa a base de datos):
```python
import mysql.connector

# Conexión manual a la base de datos
connection = mysql.connector.connect(
    host='localhost',
    database='erp_database',
    user='admin',
    password='password123'
)

def crear_cliente(nombre, email, telefono):
    cursor = connection.cursor()
    query = "INSERT INTO clientes (nombre, email, telefono) VALUES (%s, %s, %s)"
    cursor.execute(query, (nombre, email, telefono))
    connection.commit()
    cursor.close()

def obtener_cliente(id_cliente):
    cursor = connection.cursor()
    query = "SELECT * FROM clientes WHERE id = %s"
    cursor.execute(query, (id_cliente,))
    resultado = cursor.fetchone()
    cursor.close()
    return resultado
```

### 🔸 **CON ORM** (Django ORM):
```python
from django.db import models

class Cliente(models.Model):
    nombre = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    telefono = models.CharField(max_length=20)

# Uso del ORM - mucho más simple
def crear_cliente(nombre, email, telefono):
    cliente = Cliente.objects.create(
        nombre=nombre,
        email=email,
        telefono=telefono
    )
    return cliente

def obtener_cliente(id_cliente):
    return Cliente.objects.get(id=id_cliente)
```

### 🔸 **Ventajas evidentes del ORM:**
- **Menos código:** No necesitamos escribir consultas SQL manuales
- **Más seguro:** Protección automática contra inyección SQL
- **Portabilidad:** Si cambiamos de MySQL a PostgreSQL, el código ORM sigue igual
- **Orientado a objetos:** Trabajamos directamente con objetos Python, no con tuplas

---

Este ejercicio me ha ayudado a entender cómo las **tecnologías de bases de datos y los ORMs** son la base sobre la que se construyen los sistemas ERP-CRM modernos.  
La elección correcta entre SQL, NoSQL o ficheros planos depende del tipo de datos y de la escala del proyecto.  
Separar las capas de conexión y lógica permite un código más profesional, limpio y fácil de mantener.  

En el contexto de la unidad de **Sistemas de gestión empresarial**, estos conceptos son esenciales para comprender cómo los ERP y CRM logran integrar diferentes áreas del negocio en un mismo sistema.  
En definitiva, aplicar estas buenas prácticas técnicas **aumenta la eficiencia operativa y la calidad del software empresarial**.