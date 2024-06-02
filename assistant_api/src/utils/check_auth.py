from functools import lru_cache

from async_fastapi_jwt_auth import AuthJWT
from async_fastapi_jwt_auth.exceptions import JWTDecodeError, MissingTokenError
from fastapi import Depends, HTTPException, Request
from models.user import User
from starlette import status


class CheckAuth:
    def __init__(self, authorize: AuthJWT):
        self._authorize = authorize

    async def check_authorization(self, request: Request):
        try:
            await self._authorize.jwt_required()
            user_id = await self._authorize.get_jwt_subject()
            role_id = (await self._authorize.get_raw_jwt())["role_id"]
            return User(user_id=user_id, role_id=role_id)

        except MissingTokenError:
            return None

        except JWTDecodeError:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Token is invalid")


@lru_cache()
def get_check_auth_service(
    authorize: AuthJWT = Depends(),
) -> CheckAuth:
    return CheckAuth(authorize)
