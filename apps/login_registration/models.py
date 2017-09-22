# -*- coding: utf-8 -*-
from __future__ import unicode_literals
import re
import bcrypt

from django.db import models
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

# Create your models here.

class usersManager(models.Manager):
    def basic_validator(self, postData):
        errors = {}
        if postData['first_name'] < 2:
            errors['first_name'] = 'Please enter a valid name'
        elif not postData['first_name'].isalpha():
            errors['first_name'] = 'Please enter a valid name'
        if postData['last_name'] < 2:
            errors['last_name'] = 'Please enter a valid name'
        elif not postData['last_name'].isalpha():
            errors['last_name'] = 'Please enter a valid name'
        if postData['email'] < 2 or not EMAIL_REGEX.match(postData['email']):
            errors['email'] = 'Please enter a valid name'
        if postData['password'] < 2:
            errors['password'] = 'Please enter a valid password'
        if postData['password'] != postData['confirm_pw']:
            errors['confirm_pw'] = 'Your passwords do not match'
        return errors
    def login(self, postData):
        errors = {}
        user = users.objects.filter(email=postData['email'])
        print user
        if user is None:
            errors['email'] = 'Invalid email'
        elif not bcrypt.checkpw(postData['password'].encode(), user[0].password.encode()):
            errors['password'] = 'Invalid password please try again'
        return errors

class users(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = usersManager()
