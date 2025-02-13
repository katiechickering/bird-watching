from flask_app.config.mysqlconnection import connect_to_mysql
from flask_app import app
from flask_app.models import user
from flask import flash

# Like class
class Like:
    DB = 'bird_watching_schema'
    def __init__(self, data):
        self.id = data['id']
        self.like = data['like']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.sighting_id = data['sighting_id']
        self.user = None

    # Get all likes
    @classmethod
    def get_likes_from_sighting(cls, data):
        id = {'id': data}
        query = '''SELECT * FROM likes LEFT JOIN users ON likes.user_id = users.id
            WHERE likes.sighting_id = %(id)s AND likes.like = 1;'''
        results = connect_to_mysql(cls.DB).query_db(query, id)
        likes = []
        for row in results:
            like = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            like.user = user.User(user_data)
            likes.append(like)
        return likes
    
    # Get like by sighting and user
    @classmethod
    def get_like(cls, data):
        query ='''SELECT * FROM likes WHERE user_id = %(user_id)s and sighting_id = %(sighting_id)s;'''
        result = connect_to_mysql(cls.DB).query_db(query, data)
        if result:
            if result[0]['like'] == 1:
                return 'like'
            else:
                return 'no_like'
        else:
            return False

    # Like a sighting
    @classmethod
    def like_sighting(cls, data):
        result = Like.get_like(data)
        if result:
            if result == 'no_like':
                query ='''UPDATE likes SET `like` = 1, updated_at = NOW() WHERE user_id = %(user_id)s AND sighting_id = %(sighting_id)s;'''
                return connect_to_mysql(cls.DB).query_db(query, data)
            else:
                return
        else:
            query ='''INSERT INTO likes (`like`, created_at, updated_at, user_id, sighting_id)
                VALUES (1, NOW(), NOW(), %(user_id)s, %(sighting_id)s);'''
            return connect_to_mysql(cls.DB).query_db(query, data)

    # Unlike a sighting
    @classmethod
    def unlike_sighting(cls, data):
        result = Like.get_like(data)
        if result:
            if result == 'like':
                query ='''UPDATE likes SET `like` = 0, updated_at = NOW() WHERE user_id = %(user_id)s AND sighting_id = %(sighting_id)s;'''
                return connect_to_mysql(cls.DB).query_db(query, data)
            else:
                return
        else:
            query ='''INSERT INTO likes (`like`, created_at, updated_at, user_id, sighting_id)
                VALUES (0, NOW(), NOW(), %(user_id)s, %(sighting_id)s);'''
            return connect_to_mysql(cls.DB).query_db(query, data)
