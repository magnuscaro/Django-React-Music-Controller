from django.db import models
import string
import random

def generateUniqueCode():
    length = 6
    while True:
        code = ''.join(random.choices(string.ascii_uppercase, k = length))
        if Room.objects.filter(roomId=code).count() == 0:
            break
    return code

# Create your models here.
class Room(models.Model):
    roomId = models.CharField(max_length=8, default=generateUniqueCode, unique=True) # Room information.
    roomHost = models.CharField(max_length=50, unique=True) #One Room has one host.
    pausePermision = models.BooleanField(null=False, default=False)
    skipVotes = models.IntegerField(null=False, default=1)
    dateCreated = models.DateTimeField(auto_now_add=True)
