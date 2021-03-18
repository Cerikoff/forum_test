from app.resources.base_resource import BaseResource


class ForumResource(BaseResource):
    def __init__(self, conn):
        super().__init__(
            conn, 
            tablename='forum',
            fields=['name', 'short_name', 'creator_user_id'],
            optional_fields=[]
        )
