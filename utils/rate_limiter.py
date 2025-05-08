from slowapi import Limiter
from slowapi.util import get_remote_address
from fastapi import Request

def get_user_id_or_ip(request: Request) -> str:
    user_id = request.headers.get("X-User-ID")
    if user_id:
        return user_id

    return request.client.host

limiter = Limiter(key_func=get_user_id_or_ip)
