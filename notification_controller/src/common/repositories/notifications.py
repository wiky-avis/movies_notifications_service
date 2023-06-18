import logging

from src.common.connectors.db import DbConnector


logger = logging.getLogger(__name__)


class NotificationsRepository:
    def __init__(self, db: DbConnector):
        self._db = db
