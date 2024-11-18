import asyncpg
from dataclasses import dataclass

@dataclass
class User:
    id: int = None
    name: str = None
    email: str = None

class UserRepository:
    def __init__(self, dsn: str):
        self.dsn = dsn
        self._pool = None

    async def initialize(self):
        # Create connection pool
        self._pool = await asyncpg.create_pool(self.dsn)
        
        # Create table if not exists
        async with self._pool.acquire() as conn:
            await conn.execute('''
                CREATE TABLE IF NOT EXISTS users (
                    id SERIAL PRIMARY KEY,
                    name TEXT NOT NULL,
                    email TEXT NOT NULL UNIQUE
                )
            ''')

    async def cleanup(self):
        if self._pool:
            await self._pool.close()

    async def add_user(self, user: User) -> User:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                'INSERT INTO users (name, email) VALUES ($1, $2) RETURNING id',
                user.name, user.email
            )
            user.id = row['id']
            return user

    async def get_user_by_id(self, user_id: int) -> User:
        async with self._pool.acquire() as conn:
            row = await conn.fetchrow(
                'SELECT id, name, email FROM users WHERE id = $1',
                user_id
            )
            if row:
                return User(
                    id=row['id'],
                    name=row['name'],
                    email=row['email']
                )
            return None
