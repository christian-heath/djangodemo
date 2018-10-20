from __future__ import unicode_literals
from django.db import models
import re
import bcrypt

PASSWORD_REGEX = re.compile(r'\d.*[A-Z]|[A-Z].*\d')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class UserManager(models.Manager):
    def registration_validator(self, postData):
        errors = {}
        if len(self.filter(email = postData['email'])) > 0:
            errors['email'] = "Email is already taken."
        if not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid email."
        if not PASSWORD_REGEX.match(postData['password']):
            errors['password'] = "Invalid password."
        if len(postData['password']) < 8:
            errors['password'] = "Password must be no fewer than 8 characters."
        if postData['password'] != postData['confirm_password']:
            errors['confirm_password'] = "Passwords do not match."
        if postData["first_name"].isalpha() != True:
            errors['first_name'] = "Invalid first name."
        if len(postData['first_name']) < 2:
            errors['first_name'] = "First name must be no fewer than 2 characters."
        if postData["last_name"].isalpha() != True:
            errors['last_name'] = "Invalid last name."
        if len(postData['last_name']) < 2:
            errors['last_name'] = "Last name must be no fewer than 2 characters."
        return errors

    def login_validator(self, postData):
        errors = {}
        if len(self.filter(email = postData['email'])) < 1:
            errors['email'] = 'Email does not exist'
            return errors
        else:
            user = self.get(email = postData['email'])
            if bcrypt.checkpw(postData['password'].encode(), user.password.encode()):
                return errors
            else:
                errors['password'] = "Invalid email/password combination."
                return errors

    def create_user(self, postData):
        create = {}
        pw_hash = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        email_hash = bcrypt.hashpw(postData['email'].encode(), bcrypt.gensalt())
        self.create(first_name = postData['first_name'], last_name=postData['last_name'], email=postData['email'], email_hash=email_hash, password=pw_hash)
        return create

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    email_hash = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)

    objects = UserManager()

class Message(models.Model):
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    user = models.ForeignKey(User, related_name="messages")

class Comment(models.Model):
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now = True)
    message = models.ForeignKey(Message, related_name="comments")
    user = models.ForeignKey(User, related_name="comments")