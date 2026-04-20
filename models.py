from core.storage import BaseStorage
from core.models import BaseModel


class Model(BaseModel):
    storage_class = BaseStorage


class Car(Model):
    fields = ['cid', 'uid', 'brand', 'model', 'plate']
    pk_field = 'cid'


class User(Model):
    fields = ['uid', 'name']
    pk_field = 'uid'


class Slot(Model):
    fields = ['sid', 'cid']
    pk_field = 'sid'

