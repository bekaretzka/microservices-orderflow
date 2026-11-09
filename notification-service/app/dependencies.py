from typing import Annotated

from fastapi import Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.service import NotificationService

def get_notification_service(
    db: Annotated[Session, Depends(get_db)]
) -> NotificationService:
    return NotificationService(session=db)