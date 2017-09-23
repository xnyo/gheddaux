import aioodbc

from utils.singleton import singleton


@singleton
class Database:
    async def connect(self, dsn, loop):
        self.pool = await aioodbc.create_pool(dsn=dsn, autocommit=True, loop=loop)

    async def dispose(self):
        if self.pool is None:
            return
        pool = self.pool
        self.pool = None
        pool.close()
        await pool.wait_closed()

    def __init__(self):
        self.pool = None

    async def fetch(self, query, arguments=None, many=False):
        if self.pool is None:
            raise RuntimeError("Connections pool has not been created yet")
        if arguments is None:
            arguments = []

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, *arguments)
                if many:
                    results = await cur.fetchall()
                    return [dict(zip([column[0] for column in cur.description], row)) for row in results]
                else:
                    result = await cur.fetchone()
                    return None if len(result) == 0 else result[0]

    async def fetch_all(self, query, arguments=None):
        return await self.fetch(query, arguments, many=True)

    async def execute(self, query, arguments=None):
        if self.pool is None:
            raise RuntimeError("Connections pool has not been created yet")
        if arguments is None:
            arguments = []

        async with self.pool.acquire() as conn:
            async with conn.cursor() as cur:
                await cur.execute(query, *arguments)