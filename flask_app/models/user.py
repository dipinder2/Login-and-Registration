from ..config.mysqlconnection import connectToMySQL
from flask import flash
import re
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 


class User:
    
    
    def __init__(self,data):
        self.id = data["id"]
        self.first_name = data["first_name"]
        self.last_name = data["last_name"]
        self.email = data["email"]
        self.password = data["password"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        
    
    @classmethod
    def add_one(cls,data):
        q = '''
            INSERT INTO users(first_name,last_name,email
            ,password) VALUES(%(first_name)s,%(last_name)s
            ,%(email)s,%(password)s)
        '''
        return connectToMySQL("users").query_db(q,data)
    
    
    @classmethod
    def get_by_email(cls,data):
        q = '''
            SELECT * FROM users WHERE email = %(email)s
        '''
        result = connectToMySQL("users").query_db(q,data)
        print('\nThe result is \n',result)
        return cls(result[0])
    
    
    @staticmethod
    def validate(data):
        is_valid = True
        login = False
        if len(data)<5:
            login = True
        if not EMAIL_REGEX.match(data['email']): 
            if login:
                flash("wrong email", 'login')
            else: 
                flash("wrong email", 'register')
            is_valid = False
        if len(data['password'])<3:
            if not login:
                flash("password needs to be more characters", 'register')
            else:
                flash("password needs to be more characters", 'login')
                return False
            is_valid = False
        if login == True:
            return True
        if len(data['first_name'])<3:
            flash("first name needs to be more characters", 'register')
            is_valid = False
        if len(data['last_name'])<3:
            flash("last name needs to be more characters", 'register')
            is_valid = False

        if data['confirmPassword'] != data['password']:
            flash("passwords don't match", 'register')
            is_valid = False
        return is_valid
