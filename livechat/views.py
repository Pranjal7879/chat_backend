from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .serializers import UserSerializer, LoginSerializer
from rest_framework.permissions import IsAuthenticated, AllowAny
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync

class CreateAccountAPIView(APIView):
    permission_classes = [AllowAny]  
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()  
            return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginApiView(APIView):
    permission_classes = []
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            return Response({
                'message': 'Login successful',
                'access_token': serializer.validated_data['access_token'],
                'refresh_token': serializer.validated_data['refresh_token']
            }, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChatAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, room_name=None):
        message = request.data.get('message', '')
        username = request.user.username
        channel_layer = get_channel_layer()
        async_to_sync(channel_layer.group_send)(
            f"chat_{room_name}",
            {
                "type": "chat_message",
                "message": message,
                "username": username,
            }
        )
        return Response({"message": "Message sent"}, status=200)