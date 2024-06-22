# DjangoLiveStreaming/views.py
from rest_framework import viewsets, permissions, status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.decorators import action, api_view, permission_classes
from django.contrib.auth import authenticate, login, logout
from rest_framework.authtoken.models import Token
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Stream, Donation, Comment
from .serializers import UserSerializer, StreamSerializer, DonationSerializer, CommentSerializer
from .dtos import ResponseDTO

User = get_user_model()

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.AllowAny]

    @action(detail=False, methods=['post'])
    def register(self, request):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response = ResponseDTO(code=200, message="User created successfully", data=UserSerializer(user).data)
            return Response(response.__dict__, status=status.HTTP_201_CREATED)
        else:
            error_messages = []
            for field, errors in serializer.errors.items():
                for error in errors:
                    error_messages.append(f"{field}: {error}")
            response = ResponseDTO(code=400, message="; ".join(error_messages), data=None)
            return Response(response.__dict__, status=status.HTTP_400_BAD_REQUEST)


def get_tokens_for_user(user):
    refresh = RefreshToken.for_user(user)
    return {
        'refresh_token': str(refresh),
        'access_token': str(refresh.access_token),
    }


@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')

    if User.objects.filter(username=username).exists():
        return Response(ResponseDTO(code=400, message="Username is already taken.", data=None).__dict__, status=400)

    if User.objects.filter(email=email).exists():
        return Response(ResponseDTO(code=400, message="Email is already registered.", data=None).__dict__, status=400)

    user = User.objects.create_user(username=username, email=email, password=password)
    user.save()

    return Response(
        ResponseDTO(code=200, message="User registered successfully.", data={"username": username, "email": email}).__dict__)


@api_view(['POST'])
@permission_classes([AllowAny])
def login_user(request):
    username = request.data.get('username')
    password = request.data.get('password')
    user = authenticate(request, username=username, password=password)
    if user is not None:
        login(request, user)
        tokens = get_tokens_for_user(user)
        return Response(ResponseDTO(code=200, message="Login successful.", data=tokens).__dict__)
    else:
        return Response(ResponseDTO(code=400, message="Invalid username or password.", data=None).__dict__, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def logout_user(request):
    try:
        refresh_token = request.data["refresh_token"]
        token = RefreshToken(refresh_token)
        token.blacklist()
        return Response(ResponseDTO(code=200, message="Logout successful.", data=None).__dict__)
    except Exception as e:
        return Response(ResponseDTO(code=400, message="Invalid token.", data=None).__dict__, status=status.HTTP_400_BAD_REQUEST)


class StreamViewSet(viewsets.ModelViewSet):
    queryset = Stream.objects.all()
    serializer_class = StreamSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(streamer=self.request.user)

    @action(detail=True, methods=['post'])
    def start(self, request, pk=None):
        stream = self.get_object()
        stream.is_active = True
        stream.save()
        response = ResponseDTO(code=200, message="Stream started", data=StreamSerializer(stream).data)
        return Response(response.__dict__)

    @action(detail=True, methods=['post'])
    def stop(self, request, pk=None):
        stream = self.get_object()
        stream.is_active = False
        stream.save()
        response = ResponseDTO(code=200, message="Stream stopped", data=StreamSerializer(stream).data)
        return Response(response.__dict__)

class DonationViewSet(viewsets.ModelViewSet):
    queryset = Donation.objects.all()
    serializer_class = DonationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(donor=self.request.user)

    @action(detail=True, methods=['post'])
    def confirm(self, request, pk=None):
        donation = self.get_object()
        donation.status = 'completed'
        donation.save()
        response = ResponseDTO(code=200, message="Donation confirmed", data=DonationSerializer(donation).data)
        return Response(response.__dict__)

class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
