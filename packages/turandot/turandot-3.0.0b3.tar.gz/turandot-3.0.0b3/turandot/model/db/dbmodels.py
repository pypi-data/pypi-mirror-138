from peewee import CharField, BooleanField, TextField, PrimaryKeyField, AutoField
from turandot.model.db.dbinit import BaseModel


class Csl(BaseModel):
    """Save path of CSL files to database"""
    dbid = AutoField(primary_key=True)
    path = TextField()


class FileSelectPersistence(BaseModel):
    """Save recently used path of file select dialogs to database"""
    input_id = TextField(primary_key=True)
    last_path = TextField(null=True)


class Templates(BaseModel):
    """Save path & allowed templating engines of templates to the database"""
    dbid = AutoField(primary_key=True)
    path = TextField()
    allow_jinja = BooleanField()
    allow_mako = BooleanField()


# Make sure tables are created before referenced
t = Templates()
c = Csl()
f = FileSelectPersistence()
