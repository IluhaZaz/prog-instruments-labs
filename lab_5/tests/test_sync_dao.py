import pytest

from sqlalchemy import inspect, select

from models.models import Role, users_table
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
    
    
    