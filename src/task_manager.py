from src.tasks import *
from src.models import Account


class TaskManager:
    @staticmethod
    async def process_checker(account: Account) -> str | bool:
        async with CheckerModule(account) as module:
            return await module.run()