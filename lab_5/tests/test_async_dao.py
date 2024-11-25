import pytest

from sqlalchemy import inspect, select

from lab_5.models.models import users_table, log_table
from lab_5.core.dao import SystemDAOAsync
from lab_5.database import async_engine, async_session_factory


@pytest.mark.asyncio
async def test_create_tables(event_loop):
    await SystemDAOAsync.create_tables()

    async with async_engine.connect() as conn:
        res = await conn.run_sync(lambda sync_conn: inspect(sync_conn).get_table_names())

    tables = {"log", "users"}
    assert tables == set(res)


users = [
  ("Safronov", "chief"),
  ("Kostenko", "worker"),
  ("Nesterenko", "user"),
  ("Lukacheva", "worker"),
  ("Borivova", "fired"),
]

@pytest.mark.asyncio
@pytest.mark.parametrize("surname, role", users)
async def test_add_user(surname: str, role: str, event_loop):
    await SystemDAOAsync.add_user(surname, role)

    async with async_session_factory() as session:
        query = select(users_table.c.surname, 
                        users_table.c.role).filter_by(surname=surname)
        res = await session.execute(query)
        res = res.all()[0]

    assert res == (surname, role)
    

@pytest.mark.asyncio
async def test_show_users(event_loop):
    res = await SystemDAOAsync.show_users()
    res.sort()
    for user1, user2 in zip(users, res):
        assert (user1[0], user1[1]) == user2[1:]


logs = [{"user_id": 1, "action": "enter"},
    {"user_id": 2, "action": "enter"},
    {"user_id": 1, "action": "quit"}
]

@pytest.mark.asyncio
async def test_add_logs(event_loop):
    await SystemDAOAsync.insert_logs(logs)

    async with async_session_factory() as session:
        query = select(log_table)
        res = await session.execute(query)
        res = res.all()
        res.sort()

    for log1, log2 in zip(logs, res):
        assert tuple(log1.values()) == log2[1:3]
        

users_to_upd = [
  (1, "Safronov", "deputy_chief"),
  (2, "Kostenko", "chief"),
  (3, None, None),
  (4, "Lukacheva", None),
  (5, None, "user"),
]


@pytest.mark.asyncio
@pytest.mark.parametrize("id, new_surname, new_role", users_to_upd)
async def test_update_worker_data(id: int, new_surname: str, new_role: str, event_loop):
    await SystemDAOAsync.update_worker_data(id, new_surname=new_surname, new_role=new_role)

    async with async_session_factory() as session:
        query = select(users_table.c.surname, 
                        users_table.c.role).filter_by(id=id)
        res = await session.execute(query)
        res = res.all()[0]

    if new_surname:
        assert new_surname == res[0]
    else:
        assert users[id - 1][0] == res[0]

    if new_role:
        assert new_role == res[1]
    else:
        assert users[id - 1][1] == res[1]


@pytest.mark.asyncio
async def test_show_logs(event_loop):
    res = await SystemDAOAsync.show_logs()

    for log1, log2 in zip(logs, res):
        assert tuple(log1.values()) == (log2[1], log2[4])