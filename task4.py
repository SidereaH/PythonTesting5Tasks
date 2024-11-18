
import asyncio
import pytest
from aiopg import connect
from sqlalchemy import MetaData, Table, Column, Integer, String, create_engine as sa_create_engine


metadata = MetaData()
test_table = Table(
    'test_table',
    metadata,
    Column('id', Integer, primary_key=True),
    Column('name', String, nullable=False)
)


async def add_record(conn, name):
    await conn.execute(test_table.insert().values(name=name))


async def get_record(conn, name):
    result = await conn.execute(test_table.select().where(test_table.c.name == name))
    return await result.fetchone()


@pytest.fixture
async def db_connection():
    dsn = "dbname=test_db user=postgres password=postgres host=127.0.0.1 port=5433"
    
    
    conn = await connect(dsn)
    async with conn.cursor() as cur:
        
        await cur.execute(f"DROP TABLE IF EXISTS {test_table.name}")
        engine = sa_create_engine(dsn)  
        metadata.create_all(engine)  
    yield conn
    await conn.close()  

@pytest.mark.asyncio
async def test_add_record(db_connection):
    
    async with db_connection.cursor() as cur:
       
        await add_record(cur, "test_name")

       
        record = await get_record(cur, "test_name")
        assert record is not None
        assert record.name == "test_name"

