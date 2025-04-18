import orjson
from pathlib import Path
from typing import Self

from better_proxy import Proxy
from pydantic import (
    BaseModel,
    ConfigDict,
    Field,
    ValidationInfo,
    field_validator,
)


class Account:
    __slots__ = (
        'mnemonic',
        'proxy'
    )

    def __init__(
        self,
        mnemonic: str,
        proxy: Proxy | None = None
    ) -> None:
        self.mnemonic = mnemonic
        self.proxy = proxy

    def __repr__(self) -> str:
        return f'Account({self.mnemonic!r})'


class DelayRange(BaseModel):
    min: int
    max: int

    @field_validator('max')
    @classmethod
    def validate_max(cls, value: int, info: ValidationInfo) -> int:
        if value < info.data['min']:
            raise ValueError('max must be greater than or equal to min')
        return value

    model_config = ConfigDict(frozen=True)


class PercentRange(BaseModel):
    min: int = Field(ge=0, le=100)
    max: int = Field(ge=0, le=100)

    @field_validator('max')
    @classmethod
    def validate_max(cls, value: int, info: ValidationInfo) -> int:
        if value < info.data['min']:
            raise ValueError('max must be greater than or equal to min')
        return value


class Config(BaseModel):
    accounts: list[Account] = Field(default_factory=list)
    threads: int
    delay_before_start: DelayRange
    module: str = ""
    route_name: str = "default"
    available_modules: list[str] = Field(default_factory=list)

    model_config = ConfigDict(
        arbitrary_types_allowed=True,
        extra='forbid',
    )

    @classmethod
    def load(cls, config_path: str | Path) -> Self:
        if isinstance(config_path, str):
            config_path = Path(config_path)
        
        try:
            raw_data = orjson.loads(config_path.read_text(encoding='utf-8'))
            return cls.model_validate(raw_data)
        except FileNotFoundError as e:
            raise FileNotFoundError(f"Config file not found: {config_path}") from e
        except orjson.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {config_path}") from e