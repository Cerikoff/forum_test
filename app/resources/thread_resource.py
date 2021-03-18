from datetime import datetime
from psycopg2 import sql

from app.resources.base_resource import BaseResource
from app.resources.updatable_mixin import UpdatableMixin


class ThreadResource(BaseResource, UpdatableMixin):
    def __init__(self, conn):
        super().__init__(
            conn, 
            tablename='thread',
            fields=['name', 'creator_user_id', 'forum_id', 'date'],
            optional_fields=['message']
        )
        self.delete_field = 'deleted'
        self.all_fields.append(self.delete_field)

    def create(self, **kwargs):
        kwargs['date'] = datetime.now()
        super().create(**kwargs)

    def delete(self, id):
        kwargs = {self.delete_field: True}
        self._update(id, self.tablename, self.delete_field, self.conn, **kwargs)

    def restore(self, id):
        kwargs = {self.delete_field: False}
        self._update(id, self.tablename, self.delete_field, self.conn, **kwargs)

    def filter(self, forum_id):
        fields = ['id', 'name']

        where = sql.SQL('where forum_id=%s') if forum_id else sql.SQL('')
        query = sql.SQL(
            'select {} from {} {}').format(
                sql.SQL(', ').join(map(sql.Identifier, fields)),
                sql.Identifier(self.tablename),
                where
            )
        
        with self.conn.cursor() as cursor:
            cursor.execute(query, (forum_id, ))
            res = cursor.fetchall()
            threads = []
            for row in res:
                threads.append(dict(zip(fields, row)))

            return threads
