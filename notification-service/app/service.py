from sqlalchemy import select
from sqlalchemy.orm import Session

from app.models import Notification
from app.config import NotFoundError

class NotificationService:
    def __init__(self, session: Session):
        self.session = session

    def get(self, notification_id: str):
        notification = self.session.get(Notification, notification_id)
        if notification is None:
            raise NotFoundError

    def get_all(self):
        stmt = select(Notification)
        return list(self.session.scalars(stmt).all())