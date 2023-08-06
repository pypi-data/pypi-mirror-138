from abc import ABC, abstractmethod
from typing import Optional, Union
from pathlib import Path
import peewee
from turandot.model.datastructures.baseasset import BaseAsset
from turandot.model.db.dbinit import BaseModel


class DatabaseAsset(BaseAsset, ABC):
    """Base class for conversion assets that are savable to and loadable from the database"""

    DB_MODEL = BaseModel
    ZERO_VALUES = [None, "0", 0]
    TITLE_NOT_FOUND_MSG = "- title not found -"

    def __init__(self, path: Union[str, Path], dbid: Optional[int] = None, expand: bool = False):
        self.dbid = dbid
        self.title = DatabaseAsset.TITLE_NOT_FOUND_MSG
        BaseAsset.__init__(self, path=path, expand=expand)

    @abstractmethod
    def _read_title(self):
        """Read title from database asset"""
        pass

    @abstractmethod
    def _to_orm(self) -> BaseModel:
        """Convert asset data to ORM model"""
        pass

    @classmethod
    @abstractmethod
    def _from_orm(cls, model: BaseModel, expand: bool):
        """Create conversion asset from database entry"""
        pass

    @classmethod
    def get(cls, dbid: int, expand: bool = False):
        """Get conversion asset by database id"""
        try:
            entry = cls.DB_MODEL.get(dbid=dbid)
        except peewee.DoesNotExist:
            return None
        return cls._from_orm(entry, expand)

    @classmethod
    def get_all(cls, expand: bool = False) -> list:
        """Get list of all database assets of this specific class"""
        objls = []
        res = cls.DB_MODEL.select().where(1)
        for i in res:
            objls.append(cls._from_orm(i, expand))
        objls.sort(key=lambda x: x.title.lower())
        return objls

    def save(self):
        """Save conversion asset to database"""
        entry = self._to_orm()
        entry.save()
        self.dbid = entry.dbid

    def delete(self):
        """Delete conversion asset from the database"""
        if self.dbid is None:
            return None
        entry = self.get(self.dbid)
        if entry is not None:
            self._to_orm().delete_instance()
