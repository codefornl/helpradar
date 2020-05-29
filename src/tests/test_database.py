import os
from unittest import TestCase
from unittest.mock import patch

from models import Db


class TestDatabase(TestCase):
    def test_default_sqlite(self):
        test_db = Db()
        assert test_db.get_db_url().startswith("sqlite")

    def test_postgres_from_env(self):
        testie = {"DB_USER": "klaas", "DB_PASSWORD": "vaak", "DB_HOST": "thuis", "DB_NAME": "1"}
        with patch.dict(os.environ, testie):
            test_db = Db()
            assert test_db.get_db_url().startswith("postgres")