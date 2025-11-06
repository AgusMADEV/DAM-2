from typing import List, Optional
from domain.models import Activity
from storage.repo_json import JsonActivityRepo
from domain.validators import valid_date, valid_duration
import logging


class ActivityService:
    def __init__(self, repo: Optional[JsonActivityRepo] = None):
        self.repo = repo or JsonActivityRepo()
        self.logger = logging.getLogger('ActivityService')

    def list_all(self) -> List[Activity]:
        return self.repo.all()

    def create(self, activity: Activity) -> Activity:
        # validations
        if not activity.title:
            raise ValueError('El título es obligatorio')
        if not valid_date(activity.date):
            raise ValueError('Fecha inválida (use YYYY-MM-DD)')
        if not valid_duration(activity.duration_min):
            raise ValueError('Duración inválida')
        self.repo.save(activity)
        self.logger.info(f'Created activity {activity.id}')
        return activity

    def update(self, activity_id: str, new_activity: Activity) -> Activity:
        existing = self.repo.find(activity_id)
        if not existing:
            raise ValueError('Actividad no encontrada')
        new_activity.id = activity_id
        self.repo.save(new_activity)
        self.logger.info(f'Updated activity {activity_id}')
        return new_activity

    def delete(self, activity_id: str):
        self.repo.delete(activity_id)
        self.logger.info(f'Deleted activity {activity_id}')

    def find(self, activity_id: str) -> Optional[Activity]:
        return self.repo.find(activity_id)

    def search(self, text: str = '', category: str = '', date_from: str = '', date_to: str = '') -> List[Activity]:
        items = self.repo.all()
        if text:
            items = [a for a in items if text.lower() in a.title.lower() or text.lower() in a.notes.lower()]
        if category:
            items = [a for a in items if a.category.lower() == category.lower()]
        if date_from:
            items = [a for a in items if a.date >= date_from]
        if date_to:
            items = [a for a in items if a.date <= date_to]
        return items
