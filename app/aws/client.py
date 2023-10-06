import aioboto3
from app.config import settings
from app.aws.constants import storage


class StorageService():
    _session = aioboto3.Session(
     aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
     aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
     region_name=settings.AWS_REGION)
    
    _bucket = settings.AWS_BUCKET
    _format = ".png"
    
    @classmethod
    def prepare_file_name(cls,file_name:str) -> str:
        if cls._format not in file_name:
            file_name += cls._format
        return file_name
    
    @classmethod
    async def async_upload_fileobj(cls,file,file_name:str) -> str:
        prepared_name = cls.prepare_file_name(file_name)
        async with cls._session.client(storage) as s3_client:
            await s3_client.upload_fileobj(file, cls._bucket, prepared_name)
        return prepared_name
        
    @classmethod
    async def async_download_fileobj(cls,file_name:str):
        async with cls._session.client(storage) as s3_client:
            s3_ob = await s3_client.get_object(Bucket=cls._bucket, Key=file_name)
            content = (await s3_ob['Body'].read())
            return content
        
        