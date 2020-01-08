from django.db import models

class User(models.Model):
    email           = models.CharField(max_length=200, unique=True)
    password        = models.CharField(max_length=200)
    phone_number    = models.CharField(max_length=11, unique=True)
    nickname        = models.CharField(max_length=100)
    introduction    = models.CharField(max_length=500, null=True)
    website         = models.URLField(max_length=2500, null=True)
    location        = models.CharField(max_length=500, null=True)
    twitter         = models.CharField(max_length=200, null=True)
    image           = models.URLField(max_length=2500, null=True)
    firstname       = models.CharField(max_length=100, null=True)
    lastname        = models.CharField(max_length=100, null=True)
    address         = models.CharField(max_length=500, null=True)
    postnumber      = models.CharField(max_length=100, null=True)
    created_at      = models.DateTimeField(auto_now_add = True)
    updated_at      = models.DateTimeField(auto_now = True)
    
    class Meta:
        db_table = 'users'