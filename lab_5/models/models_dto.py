from pydantic import BaseModel

from models import Action, Role


class LogTablePostDTO(BaseModel):
    user_id: int
    action: Action


class LogTableDTO(LogTablePostDTO):
    id: int
    at: int


class LogTableRelDTO(LogTableDTO):
    user: "UsersTableDTO"


class UsersTablePostDTO(BaseModel):
    surname: str
    role: Role


class UsersTableDTO(UsersTablePostDTO):
    id: int


class UsersTableRelDTO(UsersTableDTO):
    logs: list["LogTableDTO"]


if __name__ == "__main__":
    from database import sync_session_factory
    from models import UsersTable
    from sqlalchemy import select
    with sync_session_factory() as session:
            query = select(UsersTable)
            res_orm = session.execute(query).scalars().all()
            res_dto = [UsersTableDTO.model_validate(user, from_attributes=True) for user in res_orm]