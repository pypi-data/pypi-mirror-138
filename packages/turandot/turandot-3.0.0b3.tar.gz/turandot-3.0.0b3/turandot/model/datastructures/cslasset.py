from typing import Optional, Union
from pathlib import Path
import peewee
from bs4 import BeautifulSoup
from turandot.model import DatabaseAsset, ConfigModel
from turandot.model.db.dbmodels import Csl


class CslAsset(DatabaseAsset):
    """Conversion asset representing a CSL file"""

    DB_MODEL = Csl

    def __init__(self, path: Union[Path, str], dbid: Optional[int] = None, expand: bool = False):
        DatabaseAsset.__init__(self, path=path, dbid=dbid, expand=expand)

    def expand(self):
        self._read_path()
        self._read_content()
        self._read_title()

    def _read_title(self):
        try:
            soup = BeautifulSoup(self.content, "xml")
            self.title = str(soup.style.info.title.contents[0])
        except Exception:
            self.title = CslAsset.TITLE_NOT_FOUND_MSG

    def _to_orm(self) -> Csl:
        try:
            entry = Csl.get(dbid=self.dbid)
        except peewee.DoesNotExist:
            return Csl.create(path=self.path)
        entry.path = self.path
        return entry

    @classmethod
    def _from_orm(cls, model: Csl, expand: bool = False):
        return cls(path=model.path, dbid=model.dbid, expand=expand)
