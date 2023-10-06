
from fastapi import HTTPException,WebSocketException,status

from app.auth.enums import Gender
from app.users.enums import Action
from app.chat.enums import ActionType



InvalidGenderException = HTTPException(status_code=400, detail=f"Invalid gender value. Allowed values: {Gender.list()}")

InvalidActionException = HTTPException(status_code=400, detail=f"Invalid action value. Allowed values: {Action.list()}")

InvalidActionTypeWebSocketException = WebSocketException(code=status.WS_1003_UNSUPPORTED_DATA, reason=f"Invalid action value. Allowed values: {ActionType.list()}")

UserAlreadyExistsException = HTTPException(status_code=500, detail=f"User already registered")


EntityFormatException = HTTPException(status_code=500, detail=f"File is not valid")


UserIsNotFoundException = HTTPException(status_code=400, detail=f"User is not registered")

InvalidUserPassowrdException = HTTPException(status_code=500, detail=f"User password is not valid")

CredentialException = HTTPException(
        status_code=401,detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"},
    )

TokenExpiredException = HTTPException(
        status_code=401,detail="Could not validate credentials, token is exipred", headers={"WWW-Authenticate": "Bearer"},
    )

ActionAddExecption = HTTPException(status_code=500, detail=f"evaluated user not exists, or current user is already rated evaluated user")

AwsNoSuchKeyException = HTTPException(status_code=500, detail=f"photo not found, photo_path is incorrect")

AwsException = HTTPException(status_code=500, detail=f"error with photo")

QuestionnairesIsOverException = HTTPException(status_code=500, detail=f"Questionnaires can not be generated for that user")

LikesIsOverException = HTTPException(status_code=500, detail=f"Not elements")