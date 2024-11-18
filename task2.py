import pytest
import aiohttp
import asyncio
import aiopg
from typing import Any
import logging

async def failing_async_function():
    await asyncio.sleep(0.1)
    raise ValueError("Expected error")

@pytest.mark.asyncio
async def test_async_function_failure():
    with pytest.raises(ValueError) as exc_info:
        await failing_async_function()
    assert str(exc_info.value) == "Expected error"
