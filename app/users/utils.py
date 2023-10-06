


from fastapi import Request


async def get_photo_url(photo_path:str,request:Request):
    photo_path_url = request.url_for("get_specifically_photo",photo_path=photo_path)
    return (photo_path_url._url).replace('http','https' if '127.0.0.1' not in photo_path_url._url else 'http')