import asyncio
import sqlite3
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Any, Iterable

import aiosqlite


class SqliteConn():

    async def connect(self, db_file: str | Path):
        self.db = await aiosqlite.connect(db_file)
        self.db.row_factory = sqlite3.Row

    async def insert(self, table: str, data: dict[str, Any]):
        async with self._lock():
            keylist = sorted(data.keys())
            fieldname_list = ','.join([f'"{x}"' for x in keylist])
            placement_list = ','.join(['?' for _ in range(len(keylist))])
            fieldvalue_list = [data[x] for x in keylist]
            async with self.db.execute(
                f'''
                INSERT INTO "{table}" ({fieldname_list}) 
                VALUES 
                    ({placement_list});
                ''',
                fieldvalue_list,
            ) as cursor:
                return cursor.lastrowid

    async def insert_many(self, table: str, data_list: list[dict[str, Any]]):
        async with self._lock():
            keylist = sorted(data_list[0].keys())
            fieldname_list = ','.join([f'`{x}`' for x in keylist])
            placement_list = ','.join(['?' for _ in range(len(keylist))])
            fieldvalue_list = [[data[x] for x in keylist] for data in data_list]
            cursor = await self.db.executemany(
                f'''
                INSERT INTO "{table}" ({fieldname_list}) 
                VALUES 
                    ({placement_list});
                ''',
                fieldvalue_list
            )
            await cursor.close()

    async def fetch_all(self, sql: str, parameters: Iterable[Any] | None = None):
        async with self._lock():
            async with self.db.execute(sql, parameters) as cursor:
                return await cursor.fetchall()

    async def fetch_one(self, sql: str, parameters: Iterable[Any] | None = None):
        async with self._lock():
            async with self.db.execute(sql, parameters) as cursor:
                return await cursor.fetchone()

    async def execute(self, sql: str, parameters: Iterable[Any] | None = None):
        async with self._lock():
            async with self.db.execute(sql, parameters) as cursor:
                return cursor.rowcount

    async def commit(self):
        async with self._lock():
            await self.db.commit()

    async def rollback(self):
        async with self._lock():
            await self.db.rollback()

    async def close(self):
        async with self._lock():
            await self.db.close()

    _is_lock: bool = False

    @asynccontextmanager
    async def _lock(self):
        while self._is_lock:
            await asyncio.sleep(0)
        self._is_lock = True
        try:
            yield
        finally:
            self._is_lock = False
