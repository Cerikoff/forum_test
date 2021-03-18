from psycopg2 import sql


class UpdatableMixin():
    def _update(self, id, tablename, updatable_fields, conn, **kwargs):
        fields = []
        for field in updatable_fields:
            if field in kwargs:
                fields.append(field)

        query = sql.SQL('update {} set ({}) = row({}) where id=%(id)s').format(
            sql.Identifier(tablename),
            sql.SQL(', ').join(map(sql.Identifier, fields)),
            sql.SQL(', ').join(map(sql.Placeholder, fields))
            )
        
        kwargs['id'] = id
        with conn.cursor() as cursor:
            cursor.execute(query, kwargs)