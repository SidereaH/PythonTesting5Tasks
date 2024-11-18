import pytest
import aiohttp
import asyncio
import aiopg
from typing import Any
import logging 
async def long_running_task() -> int:
    await asyncio.sleep(2)
    return 42

async def run_in_thread(func: callable) -> Any:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, func)

def blocking_wrapper():
    async def _run():
        return await long_running_task()
    
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    result = loop.run_until_complete(_run())
    loop.close()
    return result

@pytest.mark.asyncio
async def test_async_in_thread():
    result = await run_in_thread(blocking_wrapper)
    assert result == 42
