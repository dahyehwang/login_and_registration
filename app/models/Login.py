from system.core.model import Model
import re

class Login(Model):
    def __init__(self):
        super(Login, self).__init__()

    def add_user(self, user):
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
        errors = []

        if not user['first_name']:
            errors.append('First name cannot be blank')
        elif len(user['first_name']) < 2:
            errors.append('First name must be at least 2 characters long')
        if not user['last_name']:
            errors.append('Last name cannot be blank')
        elif len(user['last_name']) < 2:
            errors.append('Last name must be at least 2 characters long')
        if not user['email']:
            errors.append('Email cannot be blank')
        elif not EMAIL_REGEX.match(user['email']):
            errors.append('Email format must be valid!')
        if not user['password']:
            errors.append('Password cannot be blank')
        elif len(user['password']) < 8:
            errors.append('Password must be at least 8 characters long')
        elif user['password'] != user['confirm_pw']:
            errors.append('Password and confirmation must match!')
        if errors:
            return {"status": False, "errors": errors}
        else:
            password = user['password']
            hashed_pw = self.bcrypt.generate_password_hash(password)
            query = "INSERT INTO users (first_name, last_name, email, password, created_at, updated_at) VALUES (:first_name, :last_name, :email, :password, NOW(), NOW())"
            data = {
            'first_name': user['first_name'],
            'last_name': user['last_name'],
            'email': user['email'],
            'password': hashed_pw
            }
            self.db.query_db(query, data)
            return {"status": True}

    def validate_user(self, user):
        query = "SELECT * FROM users WHERE email = :temp_email"
        data = {'temp_email': user['email']}
        return self.db.query_db(query, data)