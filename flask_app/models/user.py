from flask_app.config.mysqlconnection import connect_to_mysql
from flask import flash
from flask_app import app
import re
from flask_bcrypt import Bcrypt

# Add bcrypt to application
bcrypt = Bcrypt(app)

# Email regular expression
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# User class
class User:
    DB = 'bird_watching_schema'
    def __init__(self, data):
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    # Validate a user registration
    @staticmethod
    def validate_reg(data):
        is_valid = True
        if len(data['fname']) < 2:
            flash('First name must be at least 2 characters', 'register')
            is_valid = False
        if len(data['lname']) < 2:
            flash('Last name must be at least 2 characters', 'register')
            is_valid = False
        if len(data['email']) < 1:
            flash('Email cannot be left blank', 'register')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email address", "register")
            is_valid = False
        elif User.get_by_email(data):
            flash("A user already exists for that email", 'register')
            is_valid = False
        if len(data['pass']) < 8:
            flash('Password must be at least 8 characters', 'register')
            is_valid = False
        elif data['confirm_pass'] != data['pass']:
            flash ('Passwords must match', 'register')
            is_valid = False
        return is_valid
    
    # Get a user by its email
    @classmethod
    def get_by_email(cls, data):
        query = 'SELECT * FROM users WHERE email = %(email)s;'
        result = connect_to_mysql(cls.DB).query_db(query, data)
        if not result:
            return False
        user = cls(result[0])
        return user

    # Register a user
    @classmethod
    def create(cls, data):
        hashed_data = {
            'fname': data['fname'],
            'lname': data['lname'],
            'email': data['email'],
            'pass': bcrypt.generate_password_hash(data['pass']), 
        }
        query = '''INSERT INTO users (first_name, last_name, email, password, created_at, updated_at)
            VALUES (%(fname)s, %(lname)s, %(email)s, %(pass)s, NOW(), NOW());'''
        return connect_to_mysql(cls.DB).query_db(query, hashed_data)
    
    # Validate a user login
    @staticmethod
    def validate_login(data):
        if len(data['email']) < 1 or len(data['pass']) < 1:
            flash('Must enter an email and password', "login")
            return False
        elif not EMAIL_REGEX.match(data['email']):
            flash("Invalid email/password", "login")
            return False
        user = User.get_by_email(data)
        if not user:
            flash("Invalid email/password", "login")
            return False
        if not bcrypt.check_password_hash(user.password, data['pass']):
            flash("Invalid email/password", "login")
            return False
        return user
    
    # Get user by id
    @classmethod
    def get_by_id(cls, data):
        id = {'id': data}
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connect_to_mysql(cls.DB).query_db(query, id)
        user = cls(result[0])
        return user
