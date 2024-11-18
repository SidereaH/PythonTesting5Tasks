import pytest
import aiohttp
import asyncio
import aiopg
from typing import Any
import logging 

async def fetch_data(url: str) -> dict:
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            return await response.json()

@pytest.mark.asyncio
async def test_http_request():
    url = "https://jsonplaceholder.typicode.com/todos/1"
    result = await fetch_data(url)
    
    assert isinstance(result, dict)
    assert "userId" in result
    assert "id" in result
    assert "title" in result
    assert "completed" in result
