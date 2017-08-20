# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

# Create your models here.
class User(models.Model):
    account = models.CharField(max_length=30, primary_key=True)
    password = models.CharField(max_length=30)
    nicheng = models.CharField(max_length=30)
    email = models.EmailField(max_length=30)
    haha = models.CharField(max_length=30)
    haha2 = models.CharField(max_length=30)

    def __unicode__(self):
        return self.account

