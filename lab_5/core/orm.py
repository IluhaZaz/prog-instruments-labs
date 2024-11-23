from sqlalchemy import select
from sqlalchemy.orm import selectinload
from tabulate import tabulate

from database import sync_engine, async_engine, sync_session_factory, async_session_factory, Base
from models.models import LogTable, Role, UsersTable


class SystemORMSync:

    @staticmethod
    def create_tables():
        sync_engine.echo = False
        Base.metadata.drop_all(sync_engine)
        Base.metadata.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_logs(logs: list[LogTable]):
        with sync_session_factory() as session:
            session.add_all(logs)
            session.commit()
    
    @staticmethod
    def show_logs(user_id: int = None):
        with sync_session_factory() as session:
            query = select(LogTable.id, 
                        LogTable.user_id, 
                        UsersTable.surname, 
                        UsersTable.role, 
                        LogTable.action, 
                        LogTable.at).join(UsersTable, UsersTable.id == LogTable.user_id)
            if user_id:
                query = query.filter_by(id=user_id)
            res = session.execute(query).all()
            print(tabulate(res, headers=("id", "user_id", "surname", "role", "action", "at"), tablefmt="double_grid"))
    
    @staticmethod
    def show_logs_by_user():
        with sync_session_factory() as session:
            query = select(UsersTable).options(selectinload(UsersTable.logs))
            result = session.execute(query).unique().scalars().all()
            res = []
            for user in result:
                res += user.logs
            res = [repr(log).split("|") for log in res]
            print(tabulate(res, headers=("id", "user_id", "action", "at"), tablefmt="double_grid"))
    
    @staticmethod
    def add_user(surname: str, role: Role):
        with sync_session_factory() as session:
            session.add(UsersTable(surname=surname, role=role))
            session.commit()

    @staticmethod
    def show_users(user_id: int = None):
        with sync_session_factory() as session:
            query = select(UsersTable)
            if user_id:
                query = query.filter_by(id=user_id)
            res = session.execute(query).scalars().all()
            res = [repr(user).split("|") for user in res]
            print(tabulate(res, headers=("id", "surname", "role"), tablefmt="double_grid"))
    
    @staticmethod
    def update_worker_data(user_id: int, new_surname: str = None, new_role: str = None):
        with sync_session_factory() as session:
            user = session.get(UsersTable, user_id)
            if new_surname:
                user.surname = new_surname
            if new_role:
                user.role = new_role
            session.commit()


class SystemORMAsync:

    @staticmethod
    async def create_tables():
        async with async_engine.connect() as conn:
            await conn.run_sync(Base.metadata.drop_all)
            await conn.run_sync(Base.metadata.create_all)
            await conn.commit()

    @staticmethod
    async def insert_logs(logs: list[LogTable]):
        async with async_session_factory() as session:
            session.add_all(logs)
            await session.commit()
    
    @staticmethod
    async def show_logs(user_id: int = None):
        async with async_session_factory() as session:
            query = select(LogTable.id, 
                        LogTable.user_id, 
                        UsersTable.surname, 
                        UsersTable.role, 
                        LogTable.action, 
                        LogTable.at).join(UsersTable, UsersTable.id == LogTable.user_id)
            if user_id:
                query = query.filter_by(id=user_id)
            res = await session.execute(query)
            res = res.all()
            print(tabulate(res, headers=("id", "user_id", "surname", "role", "action", "at"), tablefmt="double_grid"))
    
    @staticmethod
    async def show_logs_by_user():
        async with async_session_factory() as session:
            query = select(UsersTable).options(selectinload(UsersTable.logs))
            result = await session.execute(query)
            result = result.unique().scalars().all()
            res = []
            for user in result:
                res += user.logs
            res = [repr(log).split("|") for log in res]
            print(tabulate(res, headers=("id", "user_id", "action", "at"), tablefmt="double_grid"))
    
    @staticmethod
    async def add_user(surname: str, role: Role):
        async with async_session_factory() as session:
            session.add(UsersTable(surname=surname, role=role))
            await session.commit()

    @staticmethod
    async def show_users(user_id: int = None):
        async with async_session_factory() as session:
            query = select(UsersTable)
            if user_id:
                query = query.filter_by(id=user_id)
            res = await session.execute(query)
            res = res.scalars().all()
            res = [repr(user).split("|") for user in res]
            print(tabulate(res, headers=("id", "surname", "role"), tablefmt="double_grid"))
    
    @staticmethod
    async def update_worker_data(user_id: int, new_surname: str = None, new_role: str = None):
        async with async_session_factory() as session:
            user = await session.get(UsersTable, user_id)
            if new_surname:
                user.surname = new_surname
            if new_role:
                user.role = new_role
            await session.commit()