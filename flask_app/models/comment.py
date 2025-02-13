from flask_app.config.mysqlconnection import connect_to_mysql
from flask_app import app
from flask_app.models import user
from flask import flash

# Comment class
class Comment:
    DB = 'bird_watching_schema'
    def __init__(self, data):
        self.id = data['id']
        self.content = data['content']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.sighting_id = data['sighting_id']
        self.user = None

    # Get all comments
    @classmethod
    def get_all(cls):
        query = '''SELECT * FROM comments LEFT JOIN users ON comments.user_id = users.id;'''
        results = connect_to_mysql(cls.DB).query_db(query)
        comments = []
        for row in results:
            comment = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.created_at']
            }
            comment.user = user.User(user_data)
            comments.append(comment)
        return comments
    
    # Create a comment
    @classmethod
    def create_comment(cls, data):
        query = '''INSERT INTO comments (content, created_at, updated_at, user_id, sighting_id)
            VALUES (%(content)s, NOW(), NOW(), %(user_id)s, %(sighting_id)s)'''
        return connect_to_mysql(cls.DB).query_db(query, data)
    
    # Validate a comment
    @classmethod
    def validate_comment(cls, data):
        is_valid = True
        if len(data['content']) < 1:
            flash("Comment must not be blank", 'comment')
            is_valid = False
        return is_valid
    
    # Delete a comment
    @classmethod
    def delete_comment(cls, data):
        query = "DELETE FROM comments WHERE id = %(id)s;"
        return connect_to_mysql(cls.DB).query_db(query, data)
    
    # Get one comment by the id
    @classmethod
    def get_by_id(cls, data):
        id = {'id': data}
        query = 'SELECT * FROM comments WHERE id = %(id)s;'
        result = connect_to_mysql(cls.DB).query_db(query, id)
        return cls(result[0])
    
    # Edit a comment
    @classmethod
    def edit(cls, data):
        query = '''UPDATE comments SET content = %(content)s, updated_at = NOW() WHERE id = %(id)s;'''
        return connect_to_mysql(cls.DB).query_db(query, data)