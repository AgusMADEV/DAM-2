from datetime import datetime, timedelta
from typing import List, Optional, Tuple, Dict
from domain import Appointment, Estado
from validators import v_fecha, v_hora, FECHA_FMT, HORA_FMT

class AppointmentStats:
    """Clase para mantener estadísticas de las citas"""
    def __init__(self):
        self.total_citas: int = 0
        self.por_estado: Dict[Estado, int] = {
            'Programada': 0,
            'Atendida': 0,
            'Cancelada': 0,
            'No presentada': 0,
            'Reprogramada': 0
        }
        self.reprogramaciones: int = 0
        self.tiempo_medio_espera: float = 0  # en días

class SlotEngine:
    def __init__(self, inicio='09:00', fin='17:00', duracion_min=30, descanso_min=0):
        self.inicio = inicio
        self.fin = fin
        self.duracion = timedelta(minutes=duracion_min)
        self.descanso = timedelta(minutes=descanso_min)

    def generar_slots(self, fecha: str) -> List[str]:
        """Devuelve lista de horas (HH:MM) posibles ese día."""
        if not v_fecha(fecha): return []
        t = datetime.strptime(self.inicio, HORA_FMT)
        end = datetime.strptime(self.fin, HORA_FMT)
        slots = []
        cur = t
        while cur + self.duracion <= end:
            slots.append(cur.strftime(HORA_FMT))
            cur = cur + self.duracion + self.descanso
        return slots

class AgendaService:
    def __init__(self, repo, slot_engine: SlotEngine):
        self.repo = repo
        self.slots = slot_engine

    def _ocupado(self, fecha: str, hora: str, excluir_id: Optional[str]=None) -> bool:
        for a in self.repo.all():
            if excluir_id and a.id == excluir_id: continue
            if a.fecha == fecha and a.hora == hora and a.estado != 'Cancelada':
                return True
        return False

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

    def editar(self, id_: str, a: Appointment):
        err = self.validar(a, editar_id=id_)
        if err: raise ValueError(err)
        a.id = id_
        self.repo.upsert(a)
        return a

    def cancelar(self, id_: str, motivo: str = ""):
        items = self.repo.all()
        for ap in items:
            if ap.id == id_:
                ap.actualizar_estado('Cancelada', motivo)
                self.repo.upsert(ap)
                return ap
        raise ValueError("Cita no encontrada")

    def marcar_estado(self, id_: str, nuevo_estado: Estado, motivo: str = ""):
        """Actualiza el estado de una cita con seguimiento"""
        items = self.repo.all()
        for ap in items:
            if ap.id == id_:
                ap.actualizar_estado(nuevo_estado, motivo)
                self.repo.upsert(ap)
                return ap
        raise ValueError("Cita no encontrada")

    def agregar_nota(self, id_: str, nota: str):
        """Agrega una nota de seguimiento a la cita"""
        items = self.repo.all()
        for ap in items:
            if ap.id == id_:
                ap.agregar_nota(nota)
                self.repo.upsert(ap)
                return ap
        raise ValueError("Cita no encontrada")

    def eliminar(self, id_: str):
        """Elimina permanentemente una cita del repositorio"""
        items = self.repo.all()
        encontrada = False
        for ap in items:
            if ap.id == id_:
                items.remove(ap)
                encontrada = True
                break
        if not encontrada:
            raise ValueError("Cita no encontrada")
        self.repo.save_many(items)
        return True

    def reprogramar_cita(self, id_: str, nueva_fecha: str, nueva_hora: str, motivo: str):
        """Reprograma una cita existente"""
        items = self.repo.all()
        for ap in items:
            if ap.id == id_:
                nueva_cita = ap.reprogramar(nueva_fecha, nueva_hora, motivo)
                # Validar la nueva cita
                err = self.validar(nueva_cita)
                if err:
                    raise ValueError(f"No se puede reprogramar: {err}")
                # Guardar ambas citas
                self.repo.upsert(ap)  # Guardar la cita original actualizada
                self.repo.upsert(nueva_cita)  # Guardar la nueva cita
                return nueva_cita
        raise ValueError("Cita no encontrada")

    def obtener_historial_paciente(self, paciente: str) -> List[Appointment]:
        """Obtiene todo el historial de citas de un paciente"""
        return [ap for ap in self.repo.all() if ap.paciente.lower() == paciente.lower()]

    def obtener_estadisticas(self) -> Dict:
        """Calcula estadísticas de las citas"""
        citas = self.repo.all()
        stats = {
            'total': len(citas),
            'estados': {},
            'reprogramaciones': 0,
            'tiempo_medio_espera': 0.0
        }
        
        # Contar estados
        for estado in ['Programada', 'Atendida', 'Cancelada', 'No presentada', 'Reprogramada']:
            stats['estados'][estado] = len([c for c in citas if c.estado == estado])
        
        # Contar reprogramaciones
        stats['reprogramaciones'] = len([c for c in citas if c.cita_anterior_id is not None])
        
        # Calcular tiempo medio de espera
        citas_programadas = [c for c in citas if c.estado in ['Programada', 'Atendida']]
        if citas_programadas:
            tiempo_espera = []
            for cita in citas_programadas:
                fecha_cita = datetime.strptime(cita.fecha, FECHA_FMT)
                fecha_creacion = datetime.fromisoformat(cita.created_at)
                dias_espera = (fecha_cita - fecha_creacion).days
                tiempo_espera.append(dias_espera)
            stats['tiempo_medio_espera'] = sum(tiempo_espera) / len(tiempo_espera)
        
        return stats

    def listar(self):
        return sorted(self.repo.all(), key=lambda x: datetime.strptime(x.fecha+" "+x.hora, FECHA_FMT+" "+HORA_FMT))

    def sugerir_siguiente(self, fecha: str) -> Optional[str]:
        ocupadas = { (a.fecha,a.hora) for a in self.repo.all() if a.estado!='Cancelada' }
        for h in self.slots.generar_slots(fecha):
            if (fecha,h) not in ocupadas:
                return h
        return None