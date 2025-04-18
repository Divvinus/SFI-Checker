import asyncio
from typing import Callable

from src.console import Console
from src.task_manager import TaskManager
from src.logger import AsyncLogger
from src.models import Account
from src.utils import get_address, random_sleep
from bot_loader import config, progress, semaphore


async def process_execution(account: Account, process_func: Callable) -> tuple[bool, str]:
    logger = AsyncLogger()

    address = get_address(account.mnemonic)
    
    async with semaphore:
        try:
            if config.delay_before_start.min > 0:
                await random_sleep(
                    address, config.delay_before_start.min, config.delay_before_start.max
                )
            result = await process_func(account)
            success = (
                result[0]
                if isinstance(result, tuple) and len(result) == 2
                else bool(result)
            )
            message = (
                result[1]
                if isinstance(result, tuple) and len(result) == 2
                else (
                    "Completed successfully" if success else "Execution failed"
                )
            )
            return success, message
        except Exception as e:
            await logger.logger_msg(
                f"Error: {str(e)}",
                address=address,
                type_msg="error", 
                method_name="process_execution"
            )
            return False, str(e)


class ModuleProcessor(AsyncLogger):
    __slots__ = ("console", "module_functions")

    def __init__(self) -> None:
        super().__init__()
        self.console = Console()
        
        self.module_functions: dict[str, Callable] = {}
        
        for module_display, module_name in Console.MODULES_DATA.items():
            if module_name in ["exit", "view_statistics"]:
                continue
                
            task_func_name = f"process_{module_name}"
            if hasattr(TaskManager, task_func_name):
                self.module_functions[module_name] = getattr(TaskManager, task_func_name)

    async def process_view_statistics(self) -> None:
        try:
            await self.logger_msg("Getting statistics...", type_msg="info")
            await self.logger_msg(f"\n📊 Processed accounts: {progress.processed}/{progress.total} 📊", type_msg="info")
                
        except Exception as e:
            await self.logger_msg(
                f"Error getting statistics: {str(e)}", 
                type_msg="error",
                method_name="process_view_statistics"
            )

    async def execute(self) -> bool:
        self.console.build()
        
        match config.module:
            case "exit":
                await self.logger_msg("🔴 Exiting program...", type_msg="info")
                return True
            case "view_statistics":
                await self.process_view_statistics()
                return False
            case module if module in self.module_functions:
                async def process_account(account): 
                    success, message = await process_execution(account, self.module_functions[module])
                    progress.increment()
                    await self.logger_msg(
                        f"Processed accounts: {progress.processed}/{progress.total}",
                        type_msg="info"
                    )
                    return success, message
                    
                tasks = []
                batch_size = config.threads
                for i in range(0, len(config.accounts), batch_size):
                    batch = config.accounts[i : i + batch_size]
                    
                    async with asyncio.TaskGroup() as tg:
                        for account in batch:
                            tasks.append(tg.create_task(process_account(account)))
                            
                    if i + batch_size < len(config.accounts):
                        await asyncio.sleep(0.5)
                
                success_count = sum(1 for task in tasks if task.result()[0])
                await self.logger_msg(f"Results of {module}:", type_msg="info")
                await self.logger_msg(f"✅ Success: {success_count}/{len(tasks)}", type_msg="info")
                await self.logger_msg(f"❌ Failed: {len(tasks) - success_count}/{len(tasks)}", type_msg="info")
                
                return False
            case _:
                await self.logger_msg(
                    f"Module {config.module} is not implemented!", 
                    type_msg="error",
                    method_name="execute"
                )
                return False