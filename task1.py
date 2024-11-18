import pytest
import aiohttp
import asyncio
import aiopg
from typing import Any
import logging

async def async_function_with_expected_result() -> str:
    await asyncio.sleep(0.1)
    return "expected result"

@pytest.mark.asyncio
async def test_async_function_success():
    result = await async_function_with_expected_result()
    assert result == "expected result"
