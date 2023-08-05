import asyncio
import enum
from .async_ import run_callback_threadsafe as run_callback_threadsafe
from types import TracebackType
from typing import Any

ZONE_GLOBAL: str

class _State(str, enum.Enum):
    INIT: str
    ACTIVE: str
    TIMEOUT: str
    EXIT: str

class _GlobalFreezeContext:
    _loop: Any
    _manager: Any
    def __init__(self, manager: TimeoutManager) -> None: ...
    async def __aenter__(self) -> _GlobalFreezeContext: ...
    async def __aexit__(self, exc_type: type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> Union[bool, None]: ...
    def __enter__(self) -> _GlobalFreezeContext: ...
    def __exit__(self, exc_type: type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> Union[bool, None]: ...
    def _enter(self) -> None: ...
    def _exit(self) -> None: ...

class _ZoneFreezeContext:
    _loop: Any
    _zone: Any
    def __init__(self, zone: _ZoneTimeoutManager) -> None: ...
    async def __aenter__(self) -> _ZoneFreezeContext: ...
    async def __aexit__(self, exc_type: type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> Union[bool, None]: ...
    def __enter__(self) -> _ZoneFreezeContext: ...
    def __exit__(self, exc_type: type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> Union[bool, None]: ...
    def _enter(self) -> None: ...
    def _exit(self) -> None: ...

class _GlobalTaskContext:
    _loop: Any
    _manager: Any
    _task: Any
    _time_left: Any
    _expiration_time: Any
    _timeout_handler: Any
    _wait_zone: Any
    _state: Any
    _cool_down: Any
    def __init__(self, manager: TimeoutManager, task: asyncio.Task[Any], timeout: float, cool_down: float) -> None: ...
    async def __aenter__(self) -> _GlobalTaskContext: ...
    async def __aexit__(self, exc_type: type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> Union[bool, None]: ...
    @property
    def state(self) -> _State: ...
    def zones_done_signal(self) -> None: ...
    def _start_timer(self) -> None: ...
    def _stop_timer(self) -> None: ...
    def _on_timeout(self) -> None: ...
    def _cancel_task(self) -> None: ...
    def pause(self) -> None: ...
    def reset(self) -> None: ...
    async def _on_wait(self) -> None: ...

class _ZoneTaskContext:
    _loop: Any
    _zone: Any
    _task: Any
    _state: Any
    _time_left: Any
    _expiration_time: Any
    _timeout_handler: Any
    def __init__(self, zone: _ZoneTimeoutManager, task: asyncio.Task[Any], timeout: float) -> None: ...
    @property
    def state(self) -> _State: ...
    async def __aenter__(self) -> _ZoneTaskContext: ...
    async def __aexit__(self, exc_type: type[BaseException], exc_val: BaseException, exc_tb: TracebackType) -> Union[bool, None]: ...
    def _start_timer(self) -> None: ...
    def _stop_timer(self) -> None: ...
    def _on_timeout(self) -> None: ...
    def pause(self) -> None: ...
    def reset(self) -> None: ...

class _ZoneTimeoutManager:
    _manager: Any
    _zone: Any
    _tasks: Any
    _freezes: Any
    def __init__(self, manager: TimeoutManager, zone: str) -> None: ...
    def __repr__(self) -> str: ...
    @property
    def name(self) -> str: ...
    @property
    def active(self) -> bool: ...
    @property
    def freezes_done(self) -> bool: ...
    def enter_task(self, task: _ZoneTaskContext) -> None: ...
    def exit_task(self, task: _ZoneTaskContext) -> None: ...
    def enter_freeze(self, freeze: _ZoneFreezeContext) -> None: ...
    def exit_freeze(self, freeze: _ZoneFreezeContext) -> None: ...
    def pause(self) -> None: ...
    def reset(self) -> None: ...

class TimeoutManager:
    _loop: Any
    _zones: Any
    _globals: Any
    _freezes: Any
    def __init__(self) -> None: ...
    @property
    def zones_done(self) -> bool: ...
    @property
    def freezes_done(self) -> bool: ...
    @property
    def zones(self) -> dict[str, _ZoneTimeoutManager]: ...
    @property
    def global_tasks(self) -> list[_GlobalTaskContext]: ...
    @property
    def global_freezes(self) -> list[_GlobalFreezeContext]: ...
    def drop_zone(self, zone_name: str) -> None: ...
    def async_timeout(self, timeout: float, zone_name: str = ..., cool_down: float = ...) -> Union[_ZoneTaskContext, _GlobalTaskContext]: ...
    def async_freeze(self, zone_name: str = ...) -> Union[_ZoneFreezeContext, _GlobalFreezeContext]: ...
    def freeze(self, zone_name: str = ...) -> Union[_ZoneFreezeContext, _GlobalFreezeContext]: ...
