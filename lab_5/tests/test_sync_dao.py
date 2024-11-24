import pytest

from sqlalchemy import inspect, select

from models.models import Role, users_table, log_table
from core.dao import SystemDAOSync
from database import sync_engine, sync_session_factory


def test_create_tables():
    SystemDAOSync.create_tables()

    inspector = inspect(sync_engine)

    tables = {"log", "users"}
    assert tables == set(inspector.get_table_names())


users = [
  ("Safronov", Role.chief),
  ("Kostenko", Role.worker),
  ("Nesterenko", Role.user),
  ("Lukacheva", Role.worker),
  ("Borivova", Role.fired),
]

@pytest.mark.parametrize("surname, role", users)
def test_add_user(surname: str, role: Role):
    SystemDAOSync.add_user(surname, role)

    with sync_session_factory() as session:
        query = select(users_table.c.surname, 
                        users_table.c.role).filter_by(surname=surname)
        res = session.execute(query).all()[0]

    assert res == (surname, role.value)
    

def test_show_users():
    res = SystemDAOSync.show_users()
    res.sort()
    for user1, user2 in zip(users, res):
        assert (user1[0], user1[1].value) == user2[1:]


logs = [{"user_id": 1, "action": "enter"},
    {"user_id": 2, "action": "enter"},
    {"user_id": 1, "action": "quit"}
]

def test_add_logs():
    SystemDAOSync.insert_logs(logs)

    with sync_session_factory() as session:
        query = select(log_table)
        res = session.execute(query).all()
        res.sort()

    for log1, log2 in zip(logs, res):
        assert tuple(log1.values()) == log2[1:3]
        

users_to_upd = [
  (1, "Safronov", Role.deputy_chief),
  (2, "Kostenko", Role.chief),
  (3, None, None),
  (4, "Lukacheva", None),
  (5, None, Role.user),
]


@pytest.mark.parametrize("id, new_surname, new_role", users_to_upd)
def test_update_worker_data(id: int, new_surname: str, new_role: Role):
    SystemDAOSync.update_worker_data(id, new_surname=new_surname, new_role=new_role)

    with sync_session_factory() as session:
        query = select(users_table.c.surname, 
                        users_table.c.role).filter_by(id=id)
        res = session.execute(query).all()[0]

    if new_surname:
        assert new_surname == res[0]
    else:
        assert users[id - 1][0] == res[0]

    if new_role:
        assert new_role.value == res[1]
    else:
        assert users[id - 1][1].value == res[1]


def test_show_logs():
    res = SystemDAOSync.show_logs()

    for log1, log2 in zip(logs, res):
        assert tuple(log1.values()) == (log2[1], log2[4])