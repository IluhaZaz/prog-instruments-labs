import logging

from typing import Optional

from fastapi import Depends, Request, Response
from fastapi_users import BaseUserManager, IntegerIDMixin, exceptions, schemas, models

from auth.utils import User, get_user_db
from config import MANAGER_SECRET as SECRET

from tasks.email_task import send_email_report_dashboard, get_email_template_dashboard


logger = logging.getLogger(__name__)

class UserManager(IntegerIDMixin, BaseUserManager[User, int]):
    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        content: str = f"<div>Dear {user.name}, you have been registred in our online shop</div>"
        email: dict[str, str] = get_email_template_dashboard(to=user.email,
                                                            theme="Successful registration",
                                                            content=content)
        send_email_report_dashboard.delay(email)

        extra={"event": "USER_REGISTER", 
                "user_id": str(user.id), 
                "data": None}
        logger.info(msg="User has been registred", extra=extra)

    async def on_after_login(self, user: User, request: Request | None = None, response: Response | None = None) -> None:
        extra={"event": "USER_LOGIN", 
                "user_id": str(user.id), 
                "data": None}
        logger.info(msg="User has logined", extra=extra)

    async def on_after_forgot_password(self, user: User, token: str, request: Request | None = None):
        content: str = f"<div>Dear {user.name}, use this token to reset your password:</div><div>{token}</div>"
        email: dict[str, str] = get_email_template_dashboard(to=user.email,
                                                            theme="Password reset",
                                                            content=content)
        send_email_report_dashboard.delay(email)

        extra={"event": "USER_PASSWORD_RESET_REQUEST", 
                "user_id": str(user.id), 
                "data": None}
        logger.info(msg="User has requested password reset", extra=extra)
    
    async def on_after_reset_password(self, user: User, request: Request | None = None) -> None:
        print(f"User {user.id} {user.email} has reseted password.")
        content: str = f"<div>Dear {user.name}, your password has been reseted</div>"
        email: dict[str, str] = get_email_template_dashboard(to=user.email,
                                                            theme="Password reset",
                                                            content=content)
        send_email_report_dashboard.delay(email)

        extra={"event": "USER_PASSWORD_RESET", 
                "user_id": str(user.id), 
                "data": None}
        logger.info(msg="User has reseted password", extra=extra)

    async def on_after_request_verify(self, user: User, token: str, request: Request | None = None) -> None:
        content: str = f"<div>Dear {user.name}, use this token to verify your email:</div><div>{token}</div>"
        email: dict[str, str] = get_email_template_dashboard(to=user.email,
                                                            theme="Email verification",
                                                            content=content)
        send_email_report_dashboard.delay(email)

        extra={"event": "USER_REQUEST_VERIFY", 
                "user_id": str(user.id), 
                "data": None}
        logger.info(msg="User has requested email verification", extra=extra)

    async def on_after_verify(self, user: User, request: Request | None = None) -> None:
        content: str = f"<div>Dear {user.name}, your email has been verified"
        email: dict[str, str] = get_email_template_dashboard(to=user.email,
                                                            theme="Email verification",
                                                            content=content)
        send_email_report_dashboard.delay(email)

        extra={"event": "USER_VERIFY", 
                "user_id": str(user.id), 
                "data": None}
        logger.info(msg="User has been verified", extra=extra)
        
    async def create(
        self,
        user_create: schemas.UC,
        safe: bool = False,
        request: Optional[Request] = None,
    ) -> models.UP:

        await self.validate_password(user_create.password, user_create)

        existing_user = await self.user_db.get_by_email(user_create.email)
        if existing_user is not None:
            extra={"event": "USER_REGISTER", 
                "user_id": None, 
                "data": None}
            logger.info(msg="User alredy exists", extra=extra)

            raise exceptions.UserAlreadyExists()

        user_dict = (
            user_create.create_update_dict()
            if safe
            else user_create.create_update_dict_superuser()
        )
        password = user_dict.pop("password")
        user_dict["hashed_password"] = self.password_helper.hash(password)
        user_dict["role_id"] = 1

        created_user = await self.user_db.create(user_dict)

        await self.on_after_register(created_user, request)

        return created_user


async def get_user_manager(user_db=Depends(get_user_db)):
    yield UserManager(user_db)