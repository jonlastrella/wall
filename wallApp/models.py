from django.db import models
import re
import bcrypt


class UserManager(models.Manager):
    def validate(self, post):
        errors = {}
        emailCheck = re.compile(
            r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post['firstName']) < 2:
            errors['firstName'] = "Your first name must be at least 2 characters!"
        if len(post['lastName']) < 2:
            errors['lastName'] = "Your last name must be at least 2 characters!"
        if len(post['password']) < 8:
            errors['password'] = "Your password must be at least 8 characters long!"
        if not emailCheck.match(post['email']):
            errors['email'] = "Invalid email!"
        if post['password'] != post['confirm']:
            errors['password'] = "Passwords do not match!"
        return errors


class User(models.Model):
    firstName = models.CharField(max_length=255)
    lastName = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()


class Message(models.Model):
    user = models.ForeignKey(
        User, related_name='messages', on_delete=models.CASCADE)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
    message = models.ForeignKey(
        Message, related_name='messageComments', on_delete=models.CASCADE)  # message id
    user = models.ForeignKey(
        User, related_name='userComments', on_delete=models.CASCADE)  # user id
    comment = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
