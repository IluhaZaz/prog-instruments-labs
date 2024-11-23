import asyncio
import argparse

from core.dao import SystemDAOSync, SystemDAOAsync
from core.orm import SystemORMSync, SystemORMAsync
from models.models import Action, LogTable, Role


parser = argparse.ArgumentParser()

dao_or_orm_group = parser.add_mutually_exclusive_group()
dao_or_orm_group.add_argument('-d', '--core', action="store_true")
dao_or_orm_group.add_argument('-o', '--orm', action="store_true")

sync_or_async = parser.add_mutually_exclusive_group()
sync_or_async.add_argument('-s', '--sync', action="store_true")
sync_or_async.add_argument('-a', '--async', action="store_true")

args = parser.parse_args()
args = dict(args._get_kwargs())

if args["sync"]:
    if args["core"]:
        SystemDAOSync.create_tables()
        SystemDAOSync.add_user("Safronov", "boss")
        SystemDAOSync.add_user("Kostenko", "worker")
        SystemDAOSync.show_users()
        SystemDAOSync.insert_logs([
            {"user_id": 1, "action": "enter"},
            {"user_id": 2, "action": "enter"},
            {"user_id": 1, "action": "quit"}
        ])
        SystemDAOSync.update_worker_data(user_id=1, new_role="worker")
        SystemDAOSync.show_logs()

    elif args["orm"]:
        SystemORMSync.create_tables()
        SystemORMSync.add_user("Safronov", Role.chief)
        SystemORMSync.add_user("Kostenko", Role.worker)
        SystemORMSync.add_user("Nesterenko", Role.user)
        SystemORMSync.add_user("Lukacheva", Role.worker)
        SystemORMSync.add_user("Borivova", Role.fired)

        SystemORMSync.update_worker_data(2, new_surname="Popov", new_role=Role.deputy_chief)

        SystemORMSync.insert_logs([
                        LogTable(user_id=1, action = Action.enter),
                        LogTable(user_id=2, action = Action.enter),
                        LogTable(user_id=1, action = Action.quit)
                        ])
        SystemORMSync.insert_logs([
                        LogTable(user_id=2, action = Action.quit),
                        LogTable(user_id=3, action = Action.enter),
                        LogTable(user_id=5, action = Action.enter),
                        LogTable(user_id=5, action = Action.quit),
                        LogTable(user_id=4, action = Action.enter),
                        LogTable(user_id=3, action = Action.quit)
                        ])
        SystemORMSync.show_users()
        SystemORMSync.show_logs()
        SystemORMSync.show_logs_by_user()

elif args["async"]:
    if args["core"]:
        async def main():
            await SystemDAOAsync.create_tables()
            await SystemDAOAsync.add_user("Safronov", "boss")
            await SystemDAOAsync.add_user("Kostenko", "worker")
            await SystemDAOAsync.show_users()
            await SystemDAOAsync.insert_logs([
                {"user_id": 1, "action": "enter"},
                {"user_id": 2, "action": "enter"},
                {"user_id": 1, "action": "quit"}
            ])
            await SystemDAOAsync.update_worker_data(user_id=1, new_role="worker")
            await SystemDAOAsync.show_logs()

        asyncio.get_event_loop().run_until_complete(main())

    elif args["orm"]:
        async def main():
            await SystemORMAsync.create_tables()
            await SystemORMAsync.add_user("Safronov", Role.chief)
            await SystemORMAsync.add_user("Kostenko", Role.worker)
            await SystemORMAsync.add_user("Nesterenko", Role.user)
            await SystemORMAsync.add_user("Lukacheva", Role.worker)
            await SystemORMAsync.add_user("Borivova", Role.fired)

            await SystemORMAsync.update_worker_data(2, new_surname="Popov", new_role=Role.deputy_chief)

            await SystemORMAsync.insert_logs([
                            LogTable(user_id=1, action = Action.enter),
                            LogTable(user_id=2, action = Action.enter),
                            LogTable(user_id=1, action = Action.quit)
                            ])
            await SystemORMAsync.insert_logs([
                            LogTable(user_id=2, action = Action.quit),
                            LogTable(user_id=3, action = Action.enter),
                            LogTable(user_id=5, action = Action.enter),
                            LogTable(user_id=5, action = Action.quit),
                            LogTable(user_id=4, action = Action.enter),
                            LogTable(user_id=3, action = Action.quit)
                            ])
            await SystemORMAsync.show_users()
            await SystemORMAsync.show_logs()
            await SystemORMAsync.show_logs_by_user()

        asyncio.get_event_loop().run_until_complete(main())