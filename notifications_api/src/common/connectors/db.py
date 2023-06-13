import logging
from typing import Optional

import asyncpg
from asyncpg import Pool

from notifications_api.src.settings import db_settings


logger = logging.getLogger(__name__)


async def get_db():
    _db = DbConnector()
    return _db


class DbConnector:
    pool: Optional[Pool] = None

    @staticmethod
    async def connect():
        try:
            DbConnector.pool = await asyncpg.create_pool(db_settings.db_url)
        except Exception:
            logger.error("Db is not initialized", exc_info=True)

    @staticmethod
    async def disconnect():
        try:
            await DbConnector.pool.close()
        except Exception:
            logger.error("Db is not disconnected", exc_info=True)
