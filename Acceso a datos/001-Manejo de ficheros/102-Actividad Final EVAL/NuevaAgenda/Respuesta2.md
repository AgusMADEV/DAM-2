He desarrollado **NuevaAgenda**, una aplicación de gestión de citas médicas que permite crear, modificar, cancelar y realizar seguimiento de citas de forma persistente utilizando archivos JSON como sistema de almacenamiento. El proyecto está diseñado para demostrar el manejo de ficheros sin necesidad de bases de datos SQL, cumpliendo así con los objetivos de la unidad.

Este sistema sirve para gestionar citas médicas en un consultorio o clínica pequeña, permitiendo:
- **Persistir datos** de citas de forma permanente en archivos JSON
- **Validar** información crítica como fechas, horas y teléfonos
- **Generar backups** en múltiples formatos (JSON y CSV)
- **Visualizar estadísticas** del estado de las citas
- **Mantener historial** de cambios y reprogramaciones

En un entorno médico real, este tipo de aplicación sería útil para pequeños consultorios que no requieren sistemas complejos de bases de datos, pero necesitan una solución confiable para gestionar su agenda diaria y mantener registros de sus pacientes.

---

### Arquitectura del Sistema

He implementado una **arquitectura en capas** que separa responsabilidades:

#### **Capa de Dominio (`domain.py`)**
Define la entidad principal `Appointment` utilizando `dataclasses`, que representa una cita médica con sus atributos y comportamientos.

```python
@dataclass
class Appointment:
    # Campos obligatorios
    fecha: DateStr
    hora: TimeStr
    paciente: str
    descripcion: str
    
    # Campos con valores por defecto
    id: str = field(default_factory=lambda: str(uuid.uuid4()))
    duracion_min: int = field(default=30)
    telefono: str = field(default="")
    estado: Estado = field(default='Programada')
    
    # Campos de seguimiento
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    updated_at: str = field(default_factory=lambda: datetime.now().isoformat())
    historial: Dict[str, str] = field(default_factory=dict)
```

**Terminología técnica:**
- **DataClass**: Decorador de Python que genera automáticamente métodos especiales como `__init__`, `__repr__`, etc.
- **Type Hints**: Anotaciones de tipo que mejoran la legibilidad y permiten detección de errores (`DateStr`, `TimeStr`, `Estado`)
- **Literal Type**: Define un conjunto cerrado de valores posibles para el estado de la cita
- **UUID**: Identificador único universal generado automáticamente para cada cita

#### **Capa de Persistencia (`storage.py`)**
Implementa el patrón **Repository** para abstraer el acceso a datos:

```python
class JsonAppointmentRepo:
    def __init__(self, path: str = 'data/appointments.json'):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    def _read(self) -> list:
        with open(self.path, 'r', encoding='utf-8') as f:
            return json.load(f)

    def _write(self, data: list):
        with open(self.path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2, ensure_ascii=False)
```

**Funcionamiento paso a paso:**
1. **Inicialización**: Crea el directorio `data/` si no existe y un archivo JSON vacío
2. **Lectura**: Abre el archivo en modo lectura, deserializa el JSON a lista de Python
3. **Escritura**: Serializa la lista de objetos a JSON con formato legible (`indent=2`)
4. **UPSERT**: Operación que actualiza si existe o inserta si no existe (Update + Insert)

#### **Capa de Validación (`validators.py`)**
Valida datos críticos antes de persistir:

```python
FECHA_FMT = '%d/%m/%Y'
HORA_FMT = '%H:%M'

def v_fecha(s: str) -> bool:
    try:
        datetime.strptime(s, FECHA_FMT)
        return True
    except Exception:
        return False

def v_telefono(s: str) -> bool:
    if not s: return True
    digits = re.sub(r'\D','', s)
    return len(digits) == 9
```

**Técnicas utilizadas:**
- **Expresiones regulares**: `re.sub(r'\D','', s)` elimina todo lo que no sea dígito
- **Parsing de fechas**: Convierte string a objeto `datetime` para validar formato
- **Validación permisiva**: El teléfono puede estar vacío pero si existe debe tener 9 dígitos

#### **Capa de Servicios (`services.py`)**
Implementa la lógica de negocio:

```python
class AgendaService:
    def validar(self, a: Appointment, editar_id: Optional[str]=None) -> Optional[str]:
        if not v_fecha(a.fecha):
            return 'Fecha inválida (usa DD/MM/YYYY)'
        if not v_hora(a.hora):
            return 'Hora inválida (usa HH:MM)'
        if self._ocupado(a.fecha, a.hora, excluir_id=editar_id):
            return 'Hueco ocupado en esa fecha y hora'
        return None

    def crear(self, a: Appointment):
        err = self.validar(a)
        if err: raise ValueError(err)
        self.repo.upsert(a)
        return a
```

**Conceptos clave:**
- **Validación en cascada**: Verifica múltiples condiciones antes de persistir
- **Detección de conflictos**: Previene citas duplicadas en la misma fecha/hora
- **Manejo de excepciones**: Lanza `ValueError` con mensaje descriptivo si hay error

### Gestión de Archivos JSON

#### **Serialización y Deserialización**
El proceso de convertir objetos Python a JSON y viceversa:

```python
# Serialización (Python → JSON)
def to_dict(self) -> dict:
    return asdict(self)  # Convierte dataclass a diccionario

# Deserialización (JSON → Python)
@classmethod
def from_dict(cls, data: dict) -> 'Appointment':
    return cls(**data)  # Expande diccionario como argumentos
```

**Flujo completo:**
1. Objeto `Appointment` → `to_dict()` → diccionario Python
2. Diccionario → `json.dump()` → string JSON → archivo
3. Archivo → `json.load()` → diccionario Python
4. Diccionario → `from_dict()` → objeto `Appointment`

#### **Manejo de Encoding**
Importante para caracteres especiales (acentos, ñ):

```python
with open(self.path, 'r', encoding='utf-8') as f:
    return json.load(f)

with open(self.path, 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=2, ensure_ascii=False)
```

- `encoding='utf-8'`: Soporta caracteres en español
- `ensure_ascii=False`: Mantiene caracteres Unicode legibles

### 2.3 Sistema de Backups

He implementado funcionalidad de respaldo en dos formatos:

```python
def hacer_backup(self):
    timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
    backup_dir = Path('backups')
    backup_dir.mkdir(exist_ok=True)
    
    # Backup JSON
    json_backup = backup_dir / f'{timestamp}-all.json'
    with open(json_backup, 'w', encoding='utf-8') as f:
        json.dump([a.to_dict() for a in self.repo.all()], f, indent=2, ensure_ascii=False)
    
    # Backup CSV
    csv_backup = backup_dir / f'{timestamp}-all.csv'
    with open(csv_backup, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=campos)
        writer.writeheader()
        writer.writerows([a.to_dict() for a in self.repo.all()])
```

**Ventajas de cada formato:**
- **JSON**: Mantiene estructura jerárquica, fácil de deserializar
- **CSV**: Compatible con Excel, más compacto, fácil de analizar

### Historial y Trazabilidad

Cada cita mantiene un registro de cambios:

```python
def actualizar_estado(self, nuevo_estado: Estado, motivo: str = "") -> None:
    timestamp = datetime.now().isoformat()
    self.historial[timestamp] = f"Cambio de estado: {self.estado} -> {nuevo_estado}. Motivo: {motivo}"
    self.estado = nuevo_estado
    self.updated_at = timestamp
    self.motivo_cambio = motivo
```

**Características:**
- **Timestamp ISO**: Formato estándar internacional (YYYY-MM-DDTHH:MM:SS)
- **Inmutabilidad del historial**: Los registros anteriores no se modifican
- **Trazabilidad completa**: Se puede auditar cualquier cambio

### Reprogramación de Citas

Sistema de vinculación entre citas reprogramadas:

```python
def reprogramar(self, nueva_fecha: DateStr, nueva_hora: TimeStr, motivo: str) -> 'Appointment':
    self.actualizar_estado('Reprogramada', motivo)
    
    nueva_cita = Appointment(
        fecha=nueva_fecha,
        hora=nueva_hora,
        duracion_min=self.duracion_min,
        paciente=self.paciente,
        telefono=self.telefono,
        descripcion=f"Reprogramada desde cita {self.id}. {self.descripcion}",
        cita_anterior_id=self.id
    )
    self.cita_siguiente_id = nueva_cita.id
    nueva_cita.agregar_nota(f"Cita reprogramada. Motivo: {motivo}")
    
    return nueva_cita
```

**Patrón de diseño:** Lista doblemente enlazada
- `cita_anterior_id`: Apunta a la cita original
- `cita_siguiente_id`: Apunta a la nueva cita
- Permite rastrear cadenas de reprogramaciones

---

### Flujo de Uso Completo

#### **Caso 1: Crear una Nueva Cita**

```python
# 1. Usuario ingresa datos en la interfaz
nueva_cita = Appointment.new(
    fecha="15/11/2025",
    hora="10:30",
    duracion_min=30,
    paciente="Juan Pérez",
    telefono="612345678",
    descripcion="Consulta general",
    estado="Programada"
)

# 2. El servicio valida los datos
try:
    agenda_service.crear(nueva_cita)
    print("Cita creada exitosamente")
except ValueError as e:
    print(f"Error: {e}")
```

**Validaciones realizadas:**
1. ✓ Fecha en formato correcto (DD/MM/YYYY)
2. ✓ Hora en formato correcto (HH:MM)
3. ✓ Teléfono con 9 dígitos
4. ✓ No existe otra cita en ese horario
5. ✓ Genera ID único automáticamente

#### **Caso 2: Leer Todas las Citas**

```python
# 1. Leer desde el repositorio
todas_las_citas = repo.all()

# 2. Filtrar por fecha
citas_hoy = [c for c in todas_las_citas if c.fecha == "12/11/2025"]

# 3. Ordenar por hora
citas_ordenadas = sorted(citas_hoy, key=lambda x: x.hora)

# 4. Mostrar
for cita in citas_ordenadas:
    print(f"{cita.hora} - {cita.paciente}: {cita.descripcion}")
```

**Salida esperada:**
```
09:00 - María López: Revisión anual
10:30 - Juan Pérez: Consulta general
14:00 - Ana García: Seguimiento
```

#### **Caso 3: Actualizar Estado de una Cita**

```python
# Marcar cita como atendida
try:
    cita = agenda_service.marcar_estado(
        id_="550e8400-e29b-41d4-a716-446655440000",
        nuevo_estado="Atendida",
        motivo="Paciente atendido sin complicaciones"
    )
    print(f"Cita actualizada: {cita.estado}")
except ValueError as e:
    print(f"Error: {e}")

# El historial ahora contiene:
# {
#   "2025-11-12T10:45:00": "Cambio de estado: Programada -> Atendida. Motivo: Paciente atendido sin complicaciones"
# }
```

#### **Caso 4: Reprogramar una Cita**

```python
# Buscar la cita original
cita_original = next((c for c in repo.all() if c.id == "abc-123"), None)

# Reprogramar
nueva_cita = cita_original.reprogramar(
    nueva_fecha="20/11/2025",
    nueva_hora="11:00",
    motivo="Paciente solicitó cambio de fecha"
)

# Guardar ambas citas actualizadas
repo.upsert(cita_original)  # Estado: Reprogramada
repo.upsert(nueva_cita)      # Estado: Programada
```

**Resultado:**
- Cita original: Estado = "Reprogramada", `cita_siguiente_id` = ID de nueva cita
- Nueva cita: Estado = "Programada", `cita_anterior_id` = ID de cita original

### Generación de Backups

```python
# Crear backup completo
timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')

# JSON backup (mantiene estructura completa)
with open(f'backups/{timestamp}-all.json', 'w', encoding='utf-8') as f:
    json.dump(
        [cita.to_dict() for cita in repo.all()],
        f,
        indent=2,
        ensure_ascii=False
    )

# CSV backup (para análisis en Excel)
with open(f'backups/{timestamp}-all.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.DictWriter(f, fieldnames=['id', 'fecha', 'hora', 'paciente', 'estado'])
    writer.writeheader()
    writer.writerows([cita.to_dict() for cita in repo.all()])
```

**Estructura de archivos generados:**
```
backups/
├── 2025-11-12-09-30-all.json
├── 2025-11-12-09-30-all.csv
├── 2025-11-12-14-15-all.json
└── 2025-11-12-14-15-all.csv
```

### Errores Comunes y Cómo Evitarlos

#### **Error 1: Formato de Fecha Incorrecto**
```python
# ❌ INCORRECTO
cita = Appointment.new(fecha="2025-11-12", ...)  # Formato americano

# ✓ CORRECTO
cita = Appointment.new(fecha="12/11/2025", ...)  # Formato DD/MM/YYYY
```

**Solución:** Siempre usar validadores antes de crear objetos:
```python
if not v_fecha("12/11/2025"):
    raise ValueError("Formato de fecha inválido")
```

#### **Error 2: Olvidar Cerrar Archivos**
```python
# ❌ INCORRECTO (puede causar pérdida de datos)
f = open('data.json', 'w')
json.dump(data, f)
# Si el programa crashea aquí, los datos no se escriben

# ✓ CORRECTO (cierre automático)
with open('data.json', 'w') as f:
    json.dump(data, f)
# El archivo se cierra automáticamente al salir del bloque
```

#### **Error 3: No Especificar Encoding**
```python
# ❌ INCORRECTO (problemas con acentos)
with open('citas.json', 'w') as f:
    json.dump(data, f)

# ✓ CORRECTO
with open('citas.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, ensure_ascii=False)
```

#### **Error 4: Duplicar IDs al Importar**
```python
# ❌ INCORRECTO (puede sobrescribir citas existentes)
nuevas_citas = json.load(f)
for cita in nuevas_citas:
    repo.upsert(Appointment.from_dict(cita))

# ✓ CORRECTO (generar nuevos IDs)
nuevas_citas = json.load(f)
for cita_data in nuevas_citas:
    cita = Appointment.from_dict(cita_data)
    cita.id = str(uuid.uuid4())  # Nuevo ID único
    repo.upsert(cita)
```

#### **Error 5: No Validar Antes de Persistir**
```python
# ❌ INCORRECTO (datos inválidos en el archivo)
repo.upsert(cita)  # Guarda sin validar

# ✓ CORRECTO (validar primero)
error = agenda_service.validar(cita)
if error:
    raise ValueError(error)
repo.upsert(cita)
```

### Ejemplo Real de Uso Completo

```python
# Inicializar el sistema
repo = JsonAppointmentRepo('data/appointments.json')
slot_engine = SlotEngine(inicio='09:00', fin='17:00', duracion_min=30)
agenda_service = AgendaService(repo, slot_engine)

# Crear cita nueva
try:
    cita = Appointment.new(
        fecha="15/11/2025",
        hora="10:00",
        duracion_min=30,
        paciente="Carlos Ruiz",
        telefono="666777888",
        descripcion="Revisión mensual"
    )
    agenda_service.crear(cita)
    print(f"✓ Cita creada con ID: {cita.id}")
except ValueError as e:
    print(f"✗ Error al crear cita: {e}")

# Listar citas del día
citas_dia = [c for c in repo.all() if c.fecha == "15/11/2025"]
print(f"\nCitas programadas: {len(citas_dia)}")
for c in sorted(citas_dia, key=lambda x: x.hora):
    print(f"  {c.hora} - {c.paciente} ({c.estado})")

# Marcar como atendida
agenda_service.marcar_estado(
    cita.id,
    "Atendida",
    "Paciente atendido correctamente"
)

# Agregar nota de seguimiento
agenda_service.agregar_nota(
    cita.id,
    "Paciente debe volver en 3 meses para control"
)

# Hacer backup
timestamp = datetime.now().strftime('%Y-%m-%d-%H-%M')
with open(f'backups/{timestamp}-all.json', 'w', encoding='utf-8') as f:
    json.dump([c.to_dict() for c in repo.all()], f, indent=2, ensure_ascii=False)
print(f"\n✓ Backup creado: backups/{timestamp}-all.json")
```

**Salida esperada:**
```
✓ Cita creada con ID: 550e8400-e29b-41d4-a716-446655440000

Citas programadas: 1
  10:00 - Carlos Ruiz (Atendida)

✓ Backup creado: backups/2025-11-12-10-30-all.json
```

---

En este proyecto he aplicado exitosamente los conceptos fundamentales de la unidad:

1. **Persistencia sin SQL**: Demostré que es posible crear sistemas robustos usando archivos JSON como almacenamiento, sin necesidad de bases de datos relacionales.

2. **Separación de responsabilidades**: Implementé una arquitectura en capas (dominio, persistencia, servicios, validación) que facilita el mantenimiento y escalabilidad del código.

3. **Manejo robusto de archivos**: Utilicé context managers (`with`), especificación de encoding UTF-8, y serialización/deserialización correcta de objetos Python a JSON.

4. **Validación de datos**: Aseguré la integridad de la información mediante validadores específicos para fechas, horas y teléfonos antes de persistir.

5. **Trazabilidad y auditoría**: Implementé sistemas de historial, timestamps y vinculación entre citas reprogramadas para mantener un registro completo de cambios.

6. **Backups en múltiples formatos**: Proporcioné funcionalidad de respaldo tanto en JSON (para restauración) como CSV (para análisis).

El desarrollo de NuevaAgenda me ha permitido comprender que **la persistencia de datos va mucho más allá de SQL**. Los archivos JSON son una alternativa válida y eficiente para aplicaciones que requieren:
- Estructura de datos flexible (no rígida como en SQL)
- Portabilidad (archivos legibles y transferibles)
- Simplicidad de implementación (sin configuración de servidores)
- Versionado fácil (pueden guardarse en Git)

Sin embargo, también he aprendido las **limitaciones**: para grandes volúmenes de datos o búsquedas complejas, una base de datos sería más eficiente. Este proyecto representa el equilibrio perfecto entre funcionalidad y simplicidad para el contexto de una agenda de consultorio pequeño.
