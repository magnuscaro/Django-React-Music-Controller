from django.shortcuts import render
from rest_framework import generics, status
from .serializers import RoomSerializer, CreateRoomSerializer
from .models import Room
from rest_framework.views import APIView
from rest_framework.response import Response


# Create your views here.


class RoomView(generics.ListAPIView):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer

class GetRoom(APIView):
    serializer_class = RoomSerializer
    lookup_url_kwarg = 'roomId'

    def get(self, request, format=None):
        roomId = request.GET.get(self.lookup_url_kwarg)
        if roomId != None:
            room = Room.objects.filter(roomId=roomId)
            if len(room) > 0:
                data = RoomSerializer(room[0]).data
                data['isHost'] = self.request.session.session_key == room[0].roomHost
                return Response(data, status=status.HTTP_200_OK)
            return Response({'Room not Found': 'Invalid Room Code.'}, status=status.HTTP_404_NOT_FOUND)
        return Response({'Bad request': 'Code parameter not found in request'}, status=status.HTTP_400_BAD_REQUEST)

class JoinRoom(APIView):
    lookup_url_kwarg = 'roomId'
    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        roomId = request.data.get(self.lookup_url_kwarg)
        if roomId != None:
            room_result = Room.objects.filter(roomId=roomId)
            if len(room_result) > 0:
                room = room_result[0]
                self.request.session['roomId'] = roomId
                return Response({'message': 'Room Joined'}, status=status.HTTP_200_OK)
            return Response({'message': 'Invalid Room Codet'}, status=status.HTTP_400_BAD_REQUEST)
        return Response({'Bad Request': 'Invalid post data, did not find a code key'}, status=status.HTTP_400_BAD_REQUEST)

class CreateRoomView(APIView):
    serializer_class = CreateRoomSerializer

    def post(self, request, format=None):
        if not self.request.session.exists(self.request.session.session_key):
            self.request.session.create()

        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            pausePermision = serializer.data.get('pausePermision')
            skipVotes = serializer.data.get('skipVotes')
            roomHost = self.request.session.session_key
            queryset = Room.objects.filter(roomHost=roomHost)
            if queryset.exists():
                room = queryset[0]
                room.pausePermision = pausePermision
                room.skipVotes = skipVotes
                room.save(update_fields=['pausePermision','skipVotes'])
                self.request.session['room_code'] = room.roomId
                return Response(RoomSerializer(room).data, status=status.HTTP_200_OK)
            else:
                room = Room(roomHost=roomHost, pausePermision=pausePermision, skipVotes=skipVotes)
                room.save()
                self.request.session['room_code'] = room.roomId
            return Response(RoomSerializer(room).data, status=status.HTTP_201_CREATED)
        return Response({'Bad Request': 'Invalid data...'}, status=status.HTTP_400_BAD_REQUEST)