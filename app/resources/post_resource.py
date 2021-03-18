from datetime import datetime
from psycopg2 import sql

from app.resources.base_resource import BaseResource
from app.resources.updatable_mixin import UpdatableMixin


class PostResource(BaseResource, UpdatableMixin):
    def __init__(self, conn):
        super().__init__(
            conn, 
            tablename='post',
            fields=['message', 'creator_user_id', 'thread_id', 'date'],
            optional_fields=[]
        )
        self.delete_field = 'deleted'
        self.all_fields.append(self.delete_field)
        self.filter_fields=['post.creator_user_id', 'post.thread_id', 'forum.forum_id']

    def create(self, **kwargs):
        kwargs['date'] = datetime.now()
        super().create(**kwargs)

    def update(self, id, **kwargs):
        self._update(id, self.tablename, self.all_fields, self.conn, **kwargs)

    def delete(self, id):
        kwargs = {self.delete_field: True}
        self._update(id, self.tablename, [self.delete_field], self.conn, **kwargs)

    def restore(self, id):
        kwargs = {self.delete_field: False}
        self._update(id, self.tablename, [self.delete_field], self.conn, **kwargs)

    def filter(self, **kwargs):
        fields = []
        for field in self.filter_fields:
            if field in kwargs:
                fields.append(
                    sql.SQL(field + '={}').format(sql.Placeholder(field)))

        where = sql.SQL('where ') if fields else sql.SQL('')
        query = sql.SQL(
            'select post.id, post.message from post left join thread ON post.thread_id = thread.id {}').format(
                where + sql.SQL(' and ').join(fields)
            )
        
        with self.conn.cursor() as cursor:
            cursor.execute(query, kwargs)
            res = cursor.fetchall()
            posts = []
            for row in res:
                posts.append(dict(zip(self.all_fields, row)))

            return posts
