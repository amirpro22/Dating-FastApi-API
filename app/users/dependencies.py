





from fastapi import Query
from app.exceptions import InvalidActionException
from app.users.enums import Action

def validate_action(action: str = Query(..., description=f"Aviable values for action: {Action.list()}")):
    if action not in Action.list():
        raise InvalidActionException
    return action
