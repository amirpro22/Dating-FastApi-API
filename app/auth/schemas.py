
import datetime
from enum import Enum
from typing import Optional

from fastapi import Depends, File, Form, HTTPException, Query, UploadFile
from pydantic import BaseModel

from app.auth.dependencies import validate_gender, validate_photo





class SAuthRegistrationParams:
    def __init__(
            self,
            email:str = Form(...),
            password:str = Form(...),
            gender:str = Depends(validate_gender),
            photo:UploadFile = Depends(validate_photo)):

            self.email = email
            self.password = password
            self.gender = gender
            self.photo = photo




class SRegisteredResponse(BaseModel):
    status : str




class SLoginRequest(BaseModel):
    email : str
    password : str

class SLoginResponse(BaseModel):
    access_token : str
    refresh_token: str
    token_type: str
