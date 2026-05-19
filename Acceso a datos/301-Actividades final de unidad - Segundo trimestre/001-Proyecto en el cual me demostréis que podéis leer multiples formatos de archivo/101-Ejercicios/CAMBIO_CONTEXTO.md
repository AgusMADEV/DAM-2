# 🍴 Cambio de Contexto: Biblioteca → Restaurantes de España

## 📋 Resumen de Cambios

El proyecto ha sido **completamente transformado** del contexto de **Biblioteca Digital** al de **Restaurantes de España**.

---

## ✅ Archivos Actualizados

### 1️⃣ **001-gestion_biblioteca.py** 
- ✅ Clase `BibliotecaDigital` → `SistemaRestaurantes`
- ✅ Datos de ejemplo: Libros → Restaurantes españoles
- ✅ Campos: ISBN/título/autor → CIF/nombre/chef/ciudad/estrellas Michelin
- ✅ Directorio: `biblioteca_datos` → `restaurantes_datos`
- ✅ Archivos generados: `restaurantes.csv` en lugar de `libros.csv`

### 2️⃣ **002-sistema_hash.py**
- ✅ Clase `BibliotecaHash` → `SistemaRestaurantesHash`
- ✅ Hash basado en CIF (en lugar de ISBN)
- ✅ 5 restaurantes con estrellas Michelin:
  - DiverXO (Madrid) - 3⭐
  - Disfrutar (Barcelona) - 3⭐
  - Quique Dacosta (Dénia) - 3⭐
  - Elkano (Getaria) - 1⭐
  - Abantal (Sevilla) - 1⭐
- ✅ Estadísticas por ciudad y estrellas Michelin

### 3️⃣ **003-serializacion_pickle.py**
- ✅ Clase `Libro` → `Restaurante`
- ✅ Clase `BibliotecaBinaria` → `SistemaRestaurantesBinario`
- ✅ Atributos: préstamos → reservas
- ✅ Métodos adaptados al contexto gastronómico

### 4️⃣ **004-esteganografia.py**
- ✅ Documentación actualizada con contexto de restaurantes
- ✅ Rutas: `biblioteca_datos` → `restaurantes_datos`

### 5️⃣ **005-explorador_directorios.py**
- ✅ Clase `ExploradorBiblioteca` → `ExploradorRestaurantes`
- ✅ Informes: `informe_biblioteca.json` → `informe_restaurantes.json`
- ✅ Mensajes y descripciones actualizadas

### 6️⃣ **006-programa_principal.py**
- ✅ Banner principal: "BIBLIOTECA DIGITAL 📚" → "RESTAURANTES DE ESPAÑA 🇪🇸"
- ✅ Título del sistema actualizado
- ✅ Menú mantiene las mismas 7 opciones

---

## 🗂️ Estructura de Datos

### Antes (Biblioteca):
```python
{
    "isbn": "978-0-13-110362-7",
    "titulo": "El Quijote",
    "autor": "Miguel de Cervantes",
    "año": "1605",
    "genero": "Novela",
    "disponible": "Si"
}
```

### Ahora (Restaurantes):
```python
{
    "cif": "A28010000",
    "nombre": "DiverXO",
    "chef": "Dabiz Muñoz",
    "ciudad": "Madrid",
    "tipo_cocina": "Fusión vanguardista",
    "estrellas_michelin": "3",
    "precio_medio": "250€"
}
```

---

## 📊 Datos de Ejemplo

Los restaurantes incluidos representan la **alta gastronomía española**:

| Restaurante | Ciudad | Chef | Estrellas | Precio |
|------------|--------|------|-----------|--------|
| DiverXO | Madrid | Dabiz Muñoz | 3⭐⭐⭐ | 250€ |
| Disfrutar | Barcelona | Oriol Castro, Eduard Xatruch, Mateu Casañas | 3⭐⭐⭐ | 220€ |
| Quique Dacosta | Dénia | Quique Dacosta | 3⭐⭐⭐ | 240€ |
| Elkano | Getaria | Pedro Arregui | 1⭐ | 100€ |
| Abantal | Sevilla | Julio Fernández | 1⭐ | 85€ |

---

## 🎯 Funcionalidades Mantenidas

Todas las funcionalidades técnicas se mantienen **intactas**:

1. ✅ **Archivos de texto**: CSV y TXT funcionando
2. ✅ **Sistema de hashes**: Búsqueda O(1) vs O(n)
3. ✅ **Serialización pickle**: Objetos complejos
4. ✅ **Esteganografía**: Ocultación en imágenes
5. ✅ **Explorador**: Árbol de directorios recursivo

---

## 🚀 Ejecución

Para probar el nuevo contexto:

```bash
# Módulo 1: Archivos de texto
python 001-gestion_biblioteca.py

# Módulo 2: Sistema de hash
python 002-sistema_hash.py

# Módulo 5: Explorador
python 005-explorador_directorios.py

# Menú completo
python 006-programa_principal.py
```

---

## 📁 Archivos Generados

El sistema ahora genera:
- `restaurantes_datos/` (directorio raíz)
- `restaurantes_datos/texto/restaurantes.csv`
- `restaurantes_datos/texto/registro.txt`
- `restaurantes_datos/hash/*.json` (5 archivos con hash MD5)
- `restaurantes_datos/logs/informe_restaurantes.json`

---

## ✨ Beneficios del Nuevo Contexto

1. **Más atractivo**: Gastronomía vs libros
2. **Datos reales**: Restaurantes españoles famosos
3. **Aplicabilidad**: Más cercano a proyectos reales (apps de reservas, guías gastronómicas)
4. **Diversidad**: Diferentes ciudades, tipos de cocina, rangos de precio
5. **Culturalmente relevante**: Patrimonio gastronómico español

---

## 📝 Notas

- Todos los módulos **funcionan correctamente** con el nuevo contexto
- Los ejemplos de código en documentación deben actualizarse
- El proyecto mantiene su objetivo pedagógico de demostrar **5 formatos de persistencia**
- Compatible con Python 3.7+

---

Fecha del cambio: **5 de marzo de 2026**
