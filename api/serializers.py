from rest_framework import serializers
from .models import Room

class RoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('id', 'roomId', 'roomHost', 'pausePermision', 
                    'skipVotes', 'dateCreated')

class CreateRoomSerializer(serializers.ModelSerializer):
    class Meta:
        model = Room
        fields = ('pausePermision', 'skipVotes')