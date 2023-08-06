from pathlib import Path
from peewee import DoesNotExist
from turandot.model.db.dbmodels import FileSelectPersistence
from turandot.model import ConfigModel


class FileSelectPersistApi:
    """Get/set recently used paths for file selector dialogs"""

    @staticmethod
    def get(selector_id: str) -> Path:
        """Get recently used path for a specific GUI element"""
        if ConfigModel().get_key(["general", "file_select_persistence"], False):
            try:
                entry = FileSelectPersistence.get(input_id=selector_id)
                return Path(entry.last_path)
            except DoesNotExist:
                pass
        return Path.home()

    @staticmethod
    def set(selector_id: str, path: Path):
        """Set recently used path for a specific GUI element"""
        try:
            entry = FileSelectPersistence.get(input_id=selector_id)
            entry.last_path = path
        except DoesNotExist:
            entry = FileSelectPersistence.create(input_id=selector_id, last_path=path)
        entry.save()
