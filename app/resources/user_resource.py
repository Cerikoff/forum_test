from psycopg2 import sql

from app.resources.base_resource import BaseResource
from app.resources.updatable_mixin import UpdatableMixin


class UserResource(BaseResource, UpdatableMixin):
    def __init__(self, conn):
        super().__init__(
            conn, 
            tablename='user',
            fields=['username'],
            optional_fields=['name', 'email']
        )

    def update(self, id, **kwargs):
        self._update(id, self.tablename, self.all_fields, self.conn, **kwargs)
