En este ejercicio trabajamos con **MongoDB**, una base de datos **NoSQL** orientada a documentos.  
A diferencia de las bases de datos relacionales, MongoDB guarda la información en **colecciones** (en lugar de tablas) y los registros se representan como **documentos JSON**.  
El objetivo del ejercicio es **insertar varios clientes** dentro de una colección llamada `clientes` y luego **consultarlos** usando el comando `find()`.  
Este tipo de operaciones son muy comunes en aplicaciones que gestionan usuarios, clientes o productos.

---
  
Primero, se selecciona o crea la base de datos con el comando:
```js
use empresadam;
```
Esto indica que a partir de ese momento trabajaremos dentro de la base de datos **empresadam**.  
Si no existe, MongoDB la crea automáticamente al guardar los primeros datos.

Después insertamos varios documentos dentro de la colección `clientes` usando `insertMany()`:

```js
db.clientes.insertMany([
    {
        nombre: "Agustín",
        apellidos: "Morcillo Aguado",
        telefono: "+34 68547859",
        email: "info@agustin.es"
    },
    {
        nombre: "Elena",
        apellidos: "Botezatu",
        telefono: "+34 123654789",
        email: "info@elena.es"
    },
    {
        nombre: "Lilo",
        apellidos: "Morcillo",
        telefono: "+34 987456321",
        email: "info@lilo.es"
    },
    {
        nombre: "Dipsy",
        apellidos: "Morcillo",
        telefono: "+34 654789321",
        email: "info@dipsy.es"
    }
]);
```

Cada documento contiene los datos básicos de un cliente: nombre, apellidos, teléfono y correo electrónico.  
MongoDB genera automáticamente el campo `_id`, que actúa como identificador único de cada documento.

Para comprobar los datos insertados, ejecutamos:
```js
db.clientes.find();
```
Esto muestra todos los documentos de la colección `clientes`, incluyendo algo similar a:
```json
{
    "_id": ObjectId("672e8f9e912e1b3b2b1a2345"),
    "nombre": "Agustín",
    "apellidos": "Morcillo Aguado",
    "telefono": "+34 68547859",
    "email": "info@agustin.es"
}
```

Si queremos buscar solo los clientes con un apellido concreto, podemos usar un filtro:
```js
db.clientes.find({ apellidos: "Morcillo" });
```

**Errores comunes a evitar:**
- Olvidar las comas entre documentos dentro del `insertMany()`.  
- Escribir mal el nombre de la colección (`cliente` en vez de `clientes`).  
- No usar llaves `{}` correctamente en los documentos.

---

Este tipo de inserciones y consultas son típicas en sistemas de gestión o paneles administrativos.  
Por ejemplo, podríamos tener una aplicación web donde los usuarios se registran y se guardan automáticamente con:
```js
db.clientes.insertOne({
    nombre: "Nuevo cliente",
    apellidos: "Ejemplo",
    telefono: "+34 600987654",
    email: "nuevo@cliente.com"
});
```

Luego, desde el panel, podríamos listar todos los registros con:
```js
db.clientes.find();
```
O filtrar clientes por ciudad, apellido o tipo de cliente según los campos almacenados.

De esta forma, el ejercicio muestra cómo MongoDB permite trabajar con datos de manera flexible y directa, sin tener que definir estructuras fijas como en SQL.

---

En resumen, este ejercicio me ayudó a comprender mejor cómo **insertar y consultar documentos** dentro de MongoDB.  
Los comandos `insertMany()` y `find()` son la base de la mayoría de operaciones CRUD (Create y Read).  
Además, trabajar con ejemplos reales como **Agustín**, **Elena**, **Lilo** y **Dipsy** hace que sea más fácil visualizar cómo se gestionan los datos de clientes dentro de una base de datos.  
Estos conceptos se conectan directamente con la unidad de **acceso a datos**, ya que enseñan a manejar información real en proyectos de desarrollo.
