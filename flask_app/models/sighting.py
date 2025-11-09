from flask_app.config.mysqlconnection import connect_to_mysql
from flask_app import app
from flask_app.models import user
from flask import flash
from datetime import datetime

# Sighting class
class Sighting:
    def __init__(self, data):
        self.id = data['id']
        self.species = data['species']
        self.location = data['location']
        self.datetime = data['datetime']
        self.number = data['number']
        self.description = data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.user = None
        self.likes = None

    # Get all sightings
    @classmethod
    def get_all(cls):
        query = '''SELECT * FROM sightings 
                   LEFT JOIN users ON sightings.user_id = users.id
                   ORDER BY sightings.datetime DESC;'''
        results = connect_to_mysql().query_db(query)
        sightings = []
        for row in results:
            sighting = cls(row)
            user_data = {
                'id': row['users.id'],
                'first_name': row['first_name'],
                'last_name': row['last_name'],
                'email': row['email'],
                'password': row['password'],
                'created_at': row['users.created_at'],
                'updated_at': row['users.updated_at']
            }
            sighting.user = user.User(user_data)

            sighting_id_dict = {'id': sighting.id}
            like_results = connect_to_mysql().query_db(
                'SELECT * FROM likes WHERE likes.sighting_id = %(id)s;', sighting_id_dict
            )
            sighting.likes = sum(1 for like_row in like_results if like_row['like'] == 1)

            sightings.append(sighting)
        return sightings

    # Delete a sighting
    @classmethod
    def delete_sighting(cls, data):
        query = "DELETE FROM sightings WHERE id = %(id)s;"
        return connect_to_mysql().query_db(query, data)

    # Validate a sighting
    @staticmethod
    def validate_sighting(data):
        is_valid = True
        if not data.get('location'):
            flash("Location is required", 'sighting')
            is_valid = False
        if not data.get('species'):
            flash("Species is required", 'sighting')
            is_valid = False
        if not data.get('datetime'):
            flash("Date and time is required", 'sighting')
            is_valid = False
        else:
            datetime_obj = datetime.fromisoformat(data['datetime'])
            if datetime_obj > datetime.now():
                flash("Date must be in the past", 'sighting')
                is_valid = False
        if not data.get('number') or int(data['number']) < 1:
            flash('Must sight at least 1 bird', 'sighting')
            is_valid = False
        if not data.get('description'):
            flash('Must provide a description', 'sighting')
            is_valid = False
        return is_valid

    # Create a sighting
    @classmethod
    def create_sighting(cls, data):
        query = '''INSERT INTO sightings 
                   (species, location, datetime, number, description, created_at, updated_at, user_id)
                   VALUES (%(species)s, %(location)s, %(datetime)s, %(number)s, %(description)s, NOW(), NOW(), %(user_id)s);'''
        return connect_to_mysql().query_db(query, data)

    # Get sighting by ID
    @classmethod
    def get_by_id(cls, sighting_id):
        id_dict = {'id': sighting_id}
        query = '''SELECT * FROM sightings 
                   LEFT JOIN users ON sightings.user_id = users.id 
                   WHERE sightings.id = %(id)s;'''
        results = connect_to_mysql().query_db(query, id_dict)
        result = results[0]
        sighting = cls(result)
        user_data = {
            'id': result['users.id'],
            'first_name': result['first_name'],
            'last_name': result['last_name'],
            'email': result['email'],
            'password': result['password'],
            'created_at': result['users.created_at'],
            'updated_at': result['users.updated_at']
        }
        sighting.user = user.User(user_data)

        like_results = connect_to_mysql().query_db(
            'SELECT * FROM likes WHERE likes.sighting_id = %(id)s;', id_dict
        )
        sighting.likes = sum(1 for like_row in like_results if like_row['like'] == 1)
        return sighting

    # Edit a sighting
    @classmethod
    def edit(cls, data):
        query = '''UPDATE sightings SET species = %(species)s, location = %(location)s, datetime = %(datetime)s,
                   number = %(number)s, description = %(description)s, updated_at = NOW() 
                   WHERE id = %(id)s;'''
        return connect_to_mysql().query_db(query, data)
