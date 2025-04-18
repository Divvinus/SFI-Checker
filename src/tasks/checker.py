from typing import Self

from src.api import BaseAPIClient
from src.wallet import Wallet
from src.logger import AsyncLogger
from src.models import Account
from src.utils.utils import update_token_balance


class CheckerModule(Wallet):
    logger = AsyncLogger()
    ATTEMPTS = 3
    
    def __init__(self, account: Account) -> None:
        Wallet.__init__(self, account.mnemonic, "https://ethereum.publicnode.com", account.proxy)
        self.account = account
        self.api_client: BaseAPIClient | None = None

    async def __aenter__(self) -> Self:
        await Wallet.__aenter__(self)
        self.api_client = BaseAPIClient(
            base_url="https://staking-mainnet.singularityfinance.ai",
            proxy=self.account.proxy
        )
        await self.api_client.__aenter__()
        return self
    
    async def __aexit__(self, exc_type, exc_val, exc_tb):
        if hasattr(self, 'api_client') and self.api_client:
            await self.api_client.__aexit__(exc_type, exc_val, exc_tb)
        await Wallet.__aexit__(self, exc_type, exc_val, exc_tb)

    def _get_headers(self) -> dict[str, str]:
        return {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'ru-RU,ru;q=0.9,en-US;q=0.8,en;q=0.7,pt;q=0.6,uk;q=0.5',
            'cache-control': 'no-cache',
            'origin': 'https://singularityfinance.ai',
            'pragma': 'no-cache',
            'priority': 'u=1, i',
            'referer': 'https://singularityfinance.ai/',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-site'
        }
        
    async def run(self) -> str | bool:
        await self.logger.logger_msg(
            msg=f"Processing checker...", 
            type_msg="info", address=self.wallet_address
        )

        try:
            for _ in range(self.ATTEMPTS):
                response = await self.api_client.send_request(
                    request_type="GET",
                    method="/staking/v1/dashboard",
                    params={'walletAddress': self.wallet_address},
                    headers=self._get_headers(),
                    verify=False
                )
                
                if response.get("status_code") == 200:
                    response = response.get("data")
                    token_amount = response.get("totalPoints")
                    
                    await self.logger.logger_msg(
                        msg=f"Token amount: {token_amount}",
                        type_msg="success", address=self.wallet_address
                    )
                    
                    await update_token_balance(self.account, token_amount)
                    
                    return token_amount
                else:
                    continue
                
            return False
        
        except Exception as e:
            await self.logger.logger_msg(
                msg=f"Critical error: {str(e)}", 
                type_msg="error", address=self.wallet_address, 
                class_name=self.__class__.__name__, method_name="run"
            )
            return False