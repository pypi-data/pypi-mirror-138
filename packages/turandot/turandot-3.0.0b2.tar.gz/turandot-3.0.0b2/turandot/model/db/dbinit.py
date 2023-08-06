import os
import shutil
import tempfile
from pathlib import Path
from peewee import DatabaseProxy, SqliteDatabase, Model, TextField
from turandot.meta import Singleton
from turandot.model import ModelUtils, ConfigModel


class DBInitializer(metaclass=Singleton):
    """Initialize SQLite database to hold templates & csl entries"""

    def __init__(self):
        self.proxy = DatabaseProxy()
        self.db = None

    # Copy initialization file if db does not exist, open db
    @staticmethod
    def _get_path() -> Path:
        """Locate SQLite file"""
        if ConfigModel().get_key(['debug', 'use_tmp_db']):
            dbpath = Path(tempfile.gettempdir()) / "turandot_assets.db"
            dbpath.unlink(missing_ok=True)
        else:
            dbpath = ModelUtils.get_config_dir() / "assets.db"
        return dbpath

    def get_db_proxy(self):
        """Use peewee proxy to init database on demand"""
        if self.db is None:
            self.db = SqliteDatabase(DBInitializer._get_path())
            self.proxy.initialize(self.db)
        return self.proxy


class BaseModel(Model):
    """Database object base model: Inherit to create tables"""

    class Meta:
        database = DBInitializer().get_db_proxy()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # slightly hacky approach to ensure table creation
        self._meta.database.create_tables([self])

    def set_data(self, **kwargs):
        """slightly hacky approach to write a dict to the db"""
        for i in self._meta.fields.keys():
            if i in kwargs.keys():
                val = kwargs[i]
                setattr(self, i, val)
