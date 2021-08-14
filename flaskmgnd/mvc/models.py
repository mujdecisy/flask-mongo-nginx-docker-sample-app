from flaskmgnd.util.pojo import Entity
from datetime import datetime

class User(Entity):
    _id: str
    username: str
    password: str

class Session(Entity):
    user_id: str
    api_key: str
    created_at: datetime
    ends_at: datetime

class Message(Entity):
    _id: str
    sender: str
    receiver: str
    send_at: datetime
    context: str
    read_already: bool