from eth_account import Account
from typing import Self
from pydantic import HttpUrl
from web3 import AsyncHTTPProvider, AsyncWeb3
from web3.eth import AsyncEth
from better_proxy import Proxy
from src.logger import AsyncLogger

logger = AsyncLogger()
Account.enable_unaudited_hdwallet_features()

class Wallet(AsyncWeb3, Account):
    def __init__(self, mnemonic: str, rpc_url: HttpUrl | str, proxy: Proxy = None):
        provider = AsyncHTTPProvider(
            str(rpc_url),
            request_kwargs={
                "proxy": proxy.as_url if proxy else None,
                "ssl": False
            }
        )

        super().__init__(provider, modules={"eth": (AsyncEth,)})
        self.keypair = self.from_mnemonic(mnemonic) if len(mnemonic.split()) in (12, 24) else self.from_key(mnemonic)
        self._is_closed = False
        
    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
        
    async def close(self):
        if self._is_closed:
            return
        
        try:
            if self.provider:
                if isinstance(self.provider, AsyncHTTPProvider):
                    await self.provider.disconnect()
                    await logger.logger_msg(
                        msg="Provider disconnected successfully", 
                        type_msg="debug", 
                        class_name=self.__class__.__name__, 
                        method_name="close"
                    )
                    
            
        except Exception as e:
            await logger.logger_msg(
                msg=f"Error during wallet cleanup: {str(e)}", 
                type_msg="warning", 
                class_name=self.__class__.__name__, 
                method_name="close"
            )
        finally:
            self._is_closed = True

    @property
    def wallet_address(self):
        return self.keypair.address