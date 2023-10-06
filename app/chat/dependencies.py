


from fastapi import Query
from app.exceptions import InvalidActionTypeWebSocketException
from app.chat.enums import ActionType

def validate_action(action: str = Query(..., description=f"Aviable values for action: {ActionType.list()}")):
    if action not in ActionType.list():
        raise InvalidActionTypeWebSocketException
    return action
