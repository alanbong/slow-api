# models.py
class BaseModel:
    storage_class = None
    pk_field = 'id'
    fields = []
    _last_pk = None

    def __init__(self):
        self.storage = self.storage_class(
           self.__class__.__name__.lower(),
           self.fields
        )

        cls = self.__class__
        if cls._last_pk is None:
            cls._last_pk = self._init_last_pk()

    def _init_last_pk(self):
        items = self.all()
        max_pk = 0

        for item in items:
            value = int(item[self.pk_field])
            if value > max_pk:
                max_pk = value

        return max_pk

    def _generate_pk(self):
        cls = self.__class__
        cls._last_pk += 1
        return cls._last_pk

    def get(self, item_id):
        result = self.filter(**{self.pk_field: item_id})
        return result[0] if result else None

    def all(self):
        return self.storage.all()

    def filter(self, **kwargs):
        return self.storage.filter(**kwargs)

    def create(self, **data):
        data[self.pk_field] = self._generate_pk()
        for field in self.fields:
            if field not in data:
                raise ValueError(f'Model missing field: {field}')
        self.storage.create(data)

    def update(self, item_id, new_data):
        data = self.all()
        for item in data:
            if str(item.get(self.pk_field)) == str(item_id):
                item.update(new_data)
                break

        self.storage.save_all(data)

    def delete(self, item_id):
        new_data = []
        for item in self.all():
            if str(item.get(self.pk_field)) != str(item_id):
                new_data.append(item)

        self.storage.save_all(new_data)
