# 🎮 Transformación a Sistema de Videojuegos

## Cambios Realizados

Este documento detalla la transformación completa del sistema de gestión de biblioteca a un sistema de gestión de videojuegos.

---

## 📊 Resumen de Cambios

### Modelos de Datos Transformados

| Modelo Original | Modelo Nuevo | Descripción |
|----------------|--------------|-------------|
| `Book` | `Game` | Representa un videojuego con plataforma, precio, rating, playtime |
| `Author` | `Studio` | Estudio de desarrollo de videojuegos |
| `User` | `Player` | Jugador con sistema de niveles basado en horas jugadas |
| `Loan` | `GameSession` | Sesión de juego/compra con tracking de horas, logros y ratings |
| `Category` | `Genre` | Género de videojuego (RPG, Action, etc.) |

---

## 🔄 Cambios en Modelos

### Game (antes Book)
```python
@dataclass
class Game(BaseEntity):
    title: str = ""
    studio_id: str = ""  # Antes: author_id
    platform: str = ""  # Nuevo: PC, PlayStation, Xbox, Nintendo Switch, Mobile
    genre: str = ""
    release_year: int = datetime.now().year  # Antes: year
    rating: float = 0.0  # Nuevo: Calificación 0-10
    price: float = 0.0  # Nuevo
    playtime_hours: int = 0  # Antes: pages
    multiplayer: bool = False  # Nuevo
    genre_id: Optional[str] = None  # Antes: category_id
    available: bool = True
```

**Campos eliminados:**
- `isbn` (no aplica a videojuegos)
- `language` (no necesario)
- `pages` (reemplazado por `playtime_hours`)

**Campos añadidos:**
- `platform`: Plataforma del juego
- `rating`: Calificación del juego (0-10)
- `price`: Precio del juego
- `playtime_hours`: Horas estimadas para completar
- `multiplayer`: Si tiene modo multijugador

---

### Studio (antes Author)
```python
@dataclass
class Studio(BaseEntity):
    name: str = ""
    founded_year: Optional[int] = None  # Antes: birth_date
    country: str = ""  # Antes: nationality
    website: str = ""  # Nuevo
    description: str = ""  # Antes: biography
```

**Cambios principales:**
- `birth_date` → `founded_year`: Año de fundación del estudio
- `nationality` → `country`: País del estudio
- Añadido `website`: Sitio web del estudio
- `name` y `last_name` → Solo `name` (nombre del estudio)

---

### Player (antes User)
```python
@dataclass
class Player(BaseEntity):
    username: str = ""  # Nuevo: reemplaza name + last_name
    email: str = ""
    password_hash: str = ""
    role: str = "player"  # Roles: player, admin, moderator (antes: user, admin, librarian)
    active: bool = True
    level: int = 1  # Nuevo: Sistema de niveles
    total_playtime_hours: float = 0.0  # Nuevo: Horas totales jugadas
```

**Cambios principales:**
- `name` + `last_name` → `username`: Nombre de usuario único
- Roles actualizados: `player`, `admin`, `moderator`
- Añadido `level`: Sistema de niveles (1 nivel por cada 10 horas jugadas)
- Añadido `total_playtime_hours`: Tracking de horas totales

**Nuevo método:**
```python
def add_playtime(self, hours: float):
    """Añadir horas de juego y actualizar nivel."""
    self.total_playtime_hours += hours
    self.level = int(self.total_playtime_hours // 10) + 1
```

---

### GameSession (antes Loan)
```python
@dataclass
class GameSession(BaseEntity):
    game_id: str = ""  # Antes: book_id
    player_id: str = ""  # Antes: user_id
    purchase_date: datetime = field(default_factory=datetime.now)  # Antes: loan_date
    playtime_hours: float = 0.0  # Nuevo
    completed: bool = False  # Nuevo
    achievements_unlocked: int = 0  # Nuevo
    last_played: Optional[datetime] = None  # Nuevo
    status: str = "active"  # active, completed, abandoned (antes: active, returned, overdue)
    rating: Optional[float] = None  # Nuevo: Rating personal del jugador
    notes: str = ""
```

**Campos eliminados:**
- `loan_date` → `purchase_date`: Fecha de compra del juego
- `due_date`: No hay concepto de "fecha límite" en videojuegos
- `return_date`: Los juegos se compran, no se devuelven
- `fine_amount`: No hay multas en videojuegos

**Campos añadidos:**
- `playtime_hours`: Horas jugadas en esta sesión
- `completed`: Si el jugador completó el juego
- `achievements_unlocked`: Logros desbloqueados
- `last_played`: Última vez que se jugó
- `rating`: Calificación personal del jugador (0-10)

**Estados actualizados:**
- `active`: Jugando activamente
- `completed`: Juego completado
- `abandoned`: Juego abandonado (reemplaza `overdue`)

---

## 🛠️ Servicios de Negocio

### GameSessionService (antes LoanService)

**Métodos transformados:**

| Método Original | Método Nuevo | Cambios |
|----------------|--------------|---------|
| `create_loan()` | `create_session()` | Crea compra de juego en lugar de préstamo |
| `return_loan()` | `add_playtime()` | Añade horas jugadas en lugar de devolver |
| `extend_loan()` | ELIMINADO | No aplica a videojuegos |
| `calculate_fines()` | ELIMINADO | No hay multas |
| `get_overdue_loans()` | ELIMINADO | No hay retrasos |

**Nuevos métodos:**
- `add_playtime(session_id, hours, achievements)`: Añadir horas y logros
- `mark_completed(session_id, rating)`: Marcar juego como completado
- `mark_abandoned(session_id)`: Marcar juego como abandonado
- `get_player_stats(player_id)`: Estadísticas del jugador
- `get_game_stats(game_id)`: Estadísticas del juego
- `get_trending_games(limit)`: Juegos en tendencia

---

## 🌐 API REST

### Nuevos Endpoints

#### Games (antes Books)
- `GET /api/games` - Listar juegos
- `GET /api/games/<id>` - Detalles del juego
- `POST /api/games` - Crear juego (admin)
- `PUT /api/games/<id>` - Actualizar juego (admin)
- `DELETE /api/games/<id>` - Eliminar juego (admin)
- `GET /api/games/platforms` - Listar plataformas
- `GET /api/games/trending` - Juegos en tendencia
- `GET /api/games/<id>/stats` - Estadísticas del juego

#### Sessions (antes Loans)
- `GET /api/sessions` - Listar sesiones
- `GET /api/sessions/<id>` - Detalles de sesión
- `POST /api/sessions` - Comprar juego
- `POST /api/sessions/<id>/playtime` - Añadir horas jugadas
- `POST /api/sessions/<id>/complete` - Marcar como completado
- `POST /api/sessions/<id>/abandon` - Marcar como abandonado
- `GET /api/sessions/player/<id>/library` - Biblioteca del jugador
- `GET /api/sessions/player/<id>/stats` - Estadísticas del jugador
- `GET /api/sessions/completed` - Sesiones completadas

---

## 📝 Compatibilidad con Código Antiguo

Para mantener compatibilidad con código existente, se han creado **aliases** en los modelos:

```python
# En models/__init__.py
Book = Game
Author = Studio
User = Player
Loan = GameSession
Category = Genre

# En business/__init__.py
LoanService = GameSessionService
```

Esto permite que código antiguo que use:
```python
framework.get_repository('Book')
framework.get_service('loan')
```

Siga funcionando mientras se adoptan los nuevos nombres:
```python
framework.get_repository('Game')
framework.get_service('session')
```

---

## 🎯 Ejemplo de Uso

```python
from data_access_framework import create_framework
from data_access_framework.models import Game, Studio, Player

# Crear framework
framework = create_framework(data_format='json')

# Crear estudio
studio = Studio(
    name='CD Projekt Red',
    founded_year=1994,
    country='Polonia',
    website='https://cdprojektred.com'
)
framework.get_repository('Studio').save(studio)

# Crear juego
game = Game(
    title='The Witcher 3: Wild Hunt',
    studio_id=studio.id,
    platform='Multi-platform',
    genre='RPG',
    release_year=2015,
    rating=9.5,
    price=39.99,
    playtime_hours=100
)
framework.get_repository('Game').save(game)

# Crear jugador
player = Player(
    username='ProGamer123',
    email='gamer@email.com',
    level=1
)
player.set_password('password123')
framework.get_repository('Player').save(player)

# Comprar juego
session_service = framework.get_service('session')
session = session_service.create_session(
    player_id=player.id,
    game_id=game.id
)

# Añadir horas de juego
session_service.add_playtime(session.id, hours=15.5, achievements=5)

# Obtener estadísticas
stats = session_service.get_player_stats(player.id)
print(f"Nivel: {stats['level']}")
print(f"Horas totales: {stats['total_playtime_hours']}")
print(f"Juegos completados: {stats['completed_games']}")
```

---

## 📚 Archivos Modificados

### Modelos
- ✅ `data_access_framework/models/__init__.py` - Nuevos modelos + aliases

### Servicios
- ✅ `data_access_framework/business/session_service.py` - Nuevo servicio
- ✅ `data_access_framework/business/__init__.py` - Exportar nuevo servicio

### API
- ✅ `data_access_framework/api/routes/games.py` - Nuevo blueprint
- ✅ `data_access_framework/api/routes/sessions.py` - Nuevo blueprint
- ✅ `data_access_framework/api/app.py` - Registrar nuevos blueprints

### Core
- ✅ `data_access_framework/core/data_access_framework.py` - Soporte para nuevas entidades

### Documentación
- ✅ `README.md` - Actualizado con contexto de videojuegos
- ✅ `ejemplo_uso.py` - Ejemplos con videojuegos
- ✅ `Actividad_FrameworkAccesoDatos_53945291X.md` - Documentación actualizada

---

## 🚀 Próximos Pasos

1. **Migrar datos existentes:** Si tienes datos de biblioteca, puedes usar el `MigrationManager` para transformarlos
2. **Actualizar código cliente:** Reemplazar referencias de `Book` → `Game`, `Loan` → `GameSession`, etc.
3. **Probar API REST:** Usar las nuevas rutas `/api/games` y `/api/sessions`
4. **Implementar nuevas funcionalidades:** Aprovechar los nuevos campos como `achievements`, `rating`, `multiplayer`

---

## 💡 Beneficios de la Transformación

- ✅ **Contexto más moderno:** Videojuegos es un dominio más atractivo
- ✅ **Funcionalidades enriquecidas:** Sistema de niveles, logros, ratings
- ✅ **API más intuitiva:** Endpoints que reflejan mejor el dominio
- ✅ **Métricas avanzadas:** Tracking de horas jugadas, tendencias, estadísticas
- ✅ **Compatibilidad mantenida:** Código antiguo sigue funcionando

---

**¡El framework está listo para gestionar tu colección de videojuegos! 🎮**
