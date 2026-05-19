En esta actividad he implementado la funcionalidad completa para cargar y visualizar poemas de Federico García Lorca en nuestra plataforma web. El objetivo principal ha sido integrar la carga de datos desde archivos JSON para mostrar tanto una lista de poemas disponibles como el detalle completo de cada poema seleccionado.

Para lograr esto, he estructurado los datos en dos niveles:
- Un archivo principal `api/poemas.json` que contiene el índice de todos los poemas organizados por libros
- Archivos individuales en `api/poemas/` que contienen el contenido completo de cada poema (título, autor, estrofas, versos, temas y símbolos)

La integración de estos datos JSON me ha permitido crear una experiencia de usuario fluida donde primero se visualiza una lista organizada de poemas y, al hacer clic en cualquier título, se carga dinámicamente el contenido completo del poema desde su archivo JSON correspondiente.

---

He seguido las mejores prácticas de programación PHP para estructurar el código de manera clara y mantenible:

**Estructura de archivos:**
- `index.php`: Controlador principal que gestiona la navegación mediante parámetros GET
- `componentes/poemas.php`: Componente que carga y lista todos los poemas
- `componentes/poema.php`: Componente que muestra el detalle de un poema individual
- `estilo.css`: Hoja de estilos que mantiene la coherencia visual

**Carga de datos JSON:**
```php
$jsonFile = 'api/poemas.json';
$jsonData = file_get_contents($jsonFile);
$data = json_decode($jsonData, true);
```

He utilizado `file_get_contents()` para leer los archivos JSON y `json_decode()` con el parámetro `true` para convertir el JSON en un array asociativo de PHP, lo que facilita el acceso a los datos.

**Seguridad:**
He implementado medidas de seguridad básicas:
- Uso de `htmlspecialchars()` para escapar caracteres especiales y prevenir XSS
- Uso de `urlencode()` para codificar correctamente los parámetros en las URLs
- Verificación de existencia del archivo antes de intentar cargarlo con `file_exists()`

**Manejo de errores:**
```php
if(file_exists($jsonFile)){
    // Cargar y mostrar poema
} else {
    echo "<h2>Error: Poema no encontrado</h2>";
}
```

**Estructura de bucles:**
He utilizado `foreach` para iterar sobre los arrays de manera eficiente, recorriendo primero los libros, luego los poemas, y finalmente las estrofas y versos.

---

**Ejemplo 1: Lista de poemas**

En el archivo `componentes/poemas.php`, implementé la carga y visualización de la lista completa:

```php
foreach ($data['obras_poeticas'] as $libro) {
    echo "<h3>" . htmlspecialchars($libro['libro']) . "</h3>\n";
    
    echo "<div class='libro-info'>";
    echo "Año: " . htmlspecialchars($libro['año']) . " | ";
    echo "Estilo: " . htmlspecialchars($libro['estilo']);
    echo "</div>\n";
    
    echo "<ul>\n";
    foreach ($libro['poemas'] as $poema) {
        echo "<li><a href='?p=poema&poema=" . urlencode($poema['titulo']) . "'>" . 
             htmlspecialchars($poema['titulo']) . "</a></li>\n";
    }
    echo "</ul>\n";
}
```

Este código muestra:
- **Libro de Poemas (1921)**
  - Canción otoñal
  - Balada triste
- **Romancero Gitano (1928)**
  - Romance de la luna, luna
  - Romance sonámbulo

Cada título es un enlace que pasa el nombre del poema como parámetro GET.

**Ejemplo 2: Visualización de poema individual**

En `componentes/poema.php`, cargo el archivo JSON específico del poema:

```php
$nombrePoema = $_GET['poema'];
$jsonFile = 'api/poemas/' . $nombrePoema . '.json';

if(file_exists($jsonFile)){
    $jsonData = file_get_contents($jsonFile);
    $poema = json_decode($jsonData, true);
    $poemaData = $poema['poema'];

    // Mostrar título y autor
    echo "<h1>" . htmlspecialchars($poemaData['titulo']) . "</h1>";
    echo "<h2>de " . htmlspecialchars($poemaData['autor']) . "</h2>";

    // Mostrar estrofas
    foreach ($poemaData['estrofas'] as $estrofa) {
        echo "<div class='estrofa'>";
        foreach ($estrofa['versos'] as $verso) {
            echo "<p>" . htmlspecialchars($verso) . "</p>";
        }
        echo "</div>";
    }
}
```

**Resultado visual:**

Cuando selecciono "Romance de la luna, luna", se muestra:

```
Romance de la luna, luna
de Federico García Lorca

La luna vino a la fragua
con su polisón de nardos.
El niño la mira, mira.
El niño la está mirando.
[...]

Temas: Muerte, Inocencia, Destino, Mundo gitano, Tragedia
Símbolos: luna, fragua, niño, gitanos, yunque
```

**Navegación implementada:**
- Página principal (?) → muestra home
- Lista de poemas (?p=poemas) → muestra todos los poemas organizados
- Poema individual (?p=poema&poema=Canción otoñal) → muestra el poema completo

---

Este ejercicio representa un hito importante en el desarrollo de nuestra plataforma de literatura poética, ya que integra los conceptos fundamentales que hemos trabajado a lo largo de la unidad:

**Integración con componentes previos:**
- Utiliza la estructura de navegación con cabecera y pie de página que ya teníamos implementados
- Mantiene la coherencia visual con `estilo.css`, asegurando una experiencia de usuario uniforme
- Se integra perfectamente con el sistema de enrutamiento basado en parámetros GET del `index.php`

**Aplicación de conceptos aprendidos:**
- **Wireframes y mockups**: La interfaz implementada respeta los diseños previos, con una lista clara de poemas y una vista detallada bien estructurada
- **Separación de responsabilidades**: Cada componente tiene una función específica (listar vs. mostrar detalle)
- **Arquitectura de datos**: La estructura JSON en dos niveles (índice + archivos individuales) permite escalabilidad y fácil mantenimiento

**Preparación para futuras mejoras:**
Esta base me permitirá, en próximas iteraciones:
- Añadir funcionalidades de búsqueda y filtrado
- Implementar favoritos o marcadores
- Agregar más autores y obras sin modificar la estructura del código
- Integrar un sistema de comentarios o valoraciones

En conclusión, he completado satisfactoriamente los tres pasos del enunciado: carga de datos JSON, visualización de lista y mostración de contenido individual. El resultado es una aplicación funcional que cumple con todas las restricciones (sin librerías externas, usando solo estructuras básicas) y que se integra perfectamente en el ecosistema de nuestra plataforma web, demostrando que los conceptos de diseño de interfaces gráficas se traducen efectivamente en código funcional y mantenible.
