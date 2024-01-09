from contextlib import AbstractContextManager
from typing import Callable
from ..core_db import DbSession
from .base_repository import BaseRepository


ADMINISTRATORS_MODEL_NAME = "administrators"


class AdminRepository(BaseRepository):
    def __init__(
        self, db_session_factory: Callable[..., AbstractContextManager[DbSession]]
    ):
        super().__init__(db_session_factory, ADMINISTRATORS_MODEL_NAME)
