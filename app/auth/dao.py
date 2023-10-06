import uuid
from app.auth.schemas import SAuthRegistrationParams
from app.auth.utils import hash_password
from app.users.dao import UsersDAO
from app.aws.client import StorageService


class AuthDAO():

    @classmethod
    async def register_user(cls,reg_params:SAuthRegistrationParams):
        photo_id = uuid.uuid4()
        file_name = await StorageService.async_upload_fileobj(reg_params.photo.file,str(photo_id))
        hashed_password = hash_password(reg_params.password)
        await UsersDAO.register_user(
            user_id=uuid.uuid4(),
            email=reg_params.email,
            password=hashed_password,
            gender=reg_params.gender,
            photo_id=photo_id,
            photo_path=file_name
        )
    