from dataclasses import dataclass, asdict, field
from datetime import datetime
from typing import Literal, Dict, Optional
import uuid

DateStr = str  # "DD/MM/YYYY"
TimeStr = str  # "HH:MM"
Estado = Literal['Programada', 'Atendida', 'Cancelada', 'No presentada', 'Reprogramada']

@dataclass
class Appointment:
    # Campos obligatorios (sin valores por defecto)
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
    notas_seguimiento: str = field(default="")
    cita_anterior_id: Optional[str] = field(default=None)
    cita_siguiente_id: Optional[str] = field(default=None)
    motivo_cambio: Optional[str] = field(default=None)

    def actualizar_estado(self, nuevo_estado: Estado, motivo: str = "") -> None:
        """Actualiza el estado de la cita y registra el cambio en el historial"""
        timestamp = datetime.now().isoformat()
        self.historial[timestamp] = f"Cambio de estado: {self.estado} -> {nuevo_estado}. Motivo: {motivo}"
        self.estado = nuevo_estado
        self.updated_at = timestamp
        self.motivo_cambio = motivo

    def agregar_nota(self, nota: str) -> None:
        """Agrega una nota de seguimiento con marca de tiempo"""
        timestamp = datetime.now().isoformat()
        self.notas_seguimiento += f"\n[{timestamp}] {nota}"
        self.updated_at = timestamp

    def reprogramar(self, nueva_fecha: DateStr, nueva_hora: TimeStr, motivo: str) -> 'Appointment':
        """Crea una nueva cita reprogramada y vincula ambas citas"""
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

    def to_dict(self) -> dict:
        """Convierte la cita a un diccionario para serialización"""
        return asdict(self)

    @classmethod
    def from_dict(cls, data: dict) -> 'Appointment':
        """Crea una instancia de Appointment desde un diccionario"""
        return cls(**data)

    @staticmethod
    def new(fecha: DateStr, hora: TimeStr, duracion_min: int, paciente: str, telefono: str, descripcion: str, estado: Estado='Programada'):
        return Appointment(
            id=str(uuid.uuid4()),
            fecha=fecha.strip(),
            hora=hora.strip(),
            duracion_min=int(duracion_min),
            paciente=paciente.strip(),
            telefono=telefono.strip(),
            descripcion=descripcion.strip(),
            estado=estado
        )

    def to_dict(self):
        return self.__dict__

    @staticmethod
    def from_dict(d):
        return Appointment(
            id=d['id'], fecha=d['fecha'], hora=d['hora'], duracion_min=int(d.get('duracion_min',30)),
            paciente=d.get('paciente',''), telefono=d.get('telefono',''), descripcion=d.get('descripcion',''), estado=d.get('estado','Programada')
        )