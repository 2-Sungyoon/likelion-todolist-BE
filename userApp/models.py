from django.db import models

# Create your models here.
class User(models.Model):

    #유저이름
    username = models.CharField(max_length=150, unique=True)
    
    #비밀번호
    password = models.CharField(max_length=150)

    def __str__(self):
        return self.username

