import datetime
from datetime import datetime
from pydantic import BaseModel, ConfigDict

class NotificationReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: str
    order_id: str
    message: str
    send_at: datetime