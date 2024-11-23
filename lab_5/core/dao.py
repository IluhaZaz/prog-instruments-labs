from sqlalchemy import select, update, insert, join
from tabulate import tabulate

from database import sync_engine, async_engine, meta_data
from models.models import log_table, users_table


class SystemDAOSync:

    @staticmethod
    def create_tables():
        sync_engine.echo = False
        meta_data.drop_all(sync_engine)
        meta_data.create_all(sync_engine)
        sync_engine.echo = True

    @staticmethod
    def insert_logs(logs: list[dict]):
        with sync_engine.connect() as conn:
            stmt = insert(table=log_table).values(logs)
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def show_logs():
        with sync_engine.connect() as conn:
            query = select(log_table.c.id, 
                        log_table.c.user_id, 
                        users_table.c.surname, 
                        users_table.c.role, 
                        log_table.c.action, 
                        log_table.c.at
                        ).select_from(
                                join(users_table, log_table, 
                                users_table.c.id == log_table.c.user_id)
                                        )
            res = conn.execute(query).all()
            print(tabulate(res, headers=("id", "user_id", "surname", "role", "action", "at"), tablefmt="double_grid"))

    @staticmethod
    def add_user(surname: str, role: str):
        with sync_engine.connect() as conn:
            stmt = insert(users_table).values([{"surname": surname, "role": role}])
            conn.execute(stmt)
            conn.commit()

    @staticmethod
    def show_users():
        with sync_engine.connect() as conn:
            query = select(users_table)
            res = conn.execute(query)
            print(tabulate(res, headers=("id", "surname", "role"), tablefmt="double_grid"))

    @staticmethod
    def update_worker_data(user_id: int, new_surname: str = None, new_role: str = None):
        with sync_engine.connect() as conn:
            if new_surname:
                stmt = update(users_table).values(surname=new_surname).filter_by(id=user_id)
                conn.execute(stmt)
            if new_role:
                stmt = update(users_table).values(role=new_role).filter_by(id=user_id)
                conn.execute(stmt)
            conn.commit()


class SystemDAOAsync:

    @staticmethod
    async def create_tables():
        async with async_engine.connect() as conn:
            await conn.run_sync(meta_data.drop_all)
            await conn.run_sync(meta_data.create_all)
            await conn.commit()
    
    @staticmethod
    async def insert_logs(logs: list[dict]):
        async with async_engine.connect() as conn:
            stmt = insert(table=log_table).values(logs)
            await conn.execute(stmt)
            await conn.commit()

    @staticmethod
    async def show_logs():
        async with async_engine.connect() as conn:
            query = select(log_table.c.id, 
                        log_table.c.user_id, 
                        users_table.c.surname, 
                        users_table.c.role, 
                        log_table.c.action, 
                        log_table.c.at
                        ).select_from(
                                join(users_table, log_table, 
                                users_table.c.id == log_table.c.user_id)
                                        )
            res = await conn.execute(query)
            res = res.all()
            print(tabulate(res, headers=("id", "user_id", "surname", "role", "action", "at"), tablefmt="double_grid"))

    @staticmethod
    async def add_user(surname: str, role: str):
        async with async_engine.connect() as conn:
            stmt = insert(users_table).values([{"surname": surname, "role": role}])
            await conn.execute(stmt)
            await conn.commit()

    @staticmethod
    async def show_users():
        async with async_engine.connect() as conn:
            query = select(users_table)
            res = await conn.execute(query)
            print(tabulate(res, headers=("id", "surname", "role"), tablefmt="double_grid"))

    @staticmethod
    async def update_worker_data(user_id: int, new_surname: str = None, new_role: str = None):
        async with async_engine.connect() as conn:
            if new_surname:
                stmt = update(users_table).values(surname=new_surname).filter_by(id=user_id)
                await conn.execute(stmt)
            if new_role:
                stmt = update(users_table).values(role=new_role).filter_by(id=user_id)
                await conn.execute(stmt)
            await conn.commit()
