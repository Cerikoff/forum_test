from psycopg2.extensions import STATUS_IN_TRANSACTION
from werkzeug.exceptions import BadRequest, NotFound
from psycopg2 import sql


class BaseResource:
    def __init__(self, conn, tablename, fields, optional_fields):
        self.conn = conn
        self.fields = fields
        self.optional_fields = optional_fields
        self.tablename = tablename
        self.all_fields = ['id'] + self.fields + self.optional_fields

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn.status == STATUS_IN_TRANSACTION:
            if exc_val:
                self.conn.rollback()
            else:
                self.conn.commit()

    def create(self, **kwargs):
        fields = []
        for field in self.fields:
            if field in kwargs:
                fields.append(field)
            else:
                raise BadRequest('{} not specified'.format(field))

        for field in self.optional_fields:
            if field in kwargs:
                fields.append(field)

        query = sql.SQL('insert into {} ({}) values ({})').format(
            sql.Identifier(self.tablename),
            sql.SQL(', ').join(map(sql.Identifier, fields)),
            sql.SQL(', ').join(map(sql.Placeholder, fields)))

        with self.conn.cursor() as cursor:
            cursor.execute(query, kwargs)

    def details(self, id):
        query = sql.SQL('select {} from {} where id=%s').format(
            sql.SQL(', ').join(map(sql.Identifier, self.all_fields)),
            sql.Identifier(self.tablename))
        
        with self.conn.cursor() as cursor:
            cursor.execute(query, (id, ))
            res = cursor.fetchone()
            if res:
                return dict(zip(self.all_fields, res))
            else:
                raise NotFound('id {} not found'.format(id))
