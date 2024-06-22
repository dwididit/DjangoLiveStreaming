# DjangoLiveStreaming/serializers.py
from rest_framework import serializers
from django.contrib.auth import get_user_model
from .models import Stream, Donation, Comment

User = get_user_model()

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'is_streamer']
        extra_kwargs = {'password': {'write_only': True}}

    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise serializers.ValidationError("A user with that username already exists.")
        return value

    def validate_email(self, value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("A user with that email already exists.")
        return value

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)
        return user

class StreamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Stream
        fields = ['id', 'title', 'description', 'streamer', 'is_active', 'created_at', 'updated_at']
        extra_kwargs = {
            'streamer': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            validated_data['streamer'] = request.user
        return super().create(validated_data)

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = ['id', 'amount', 'message', 'stream', 'donor', 'payment_method', 'status', 'transaction_id', 'created_at', 'updated_at']
        extra_kwargs = {
            'donor': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            validated_data['donor'] = request.user
        return super().create(validated_data)

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'content', 'stream', 'user', 'created_at', 'updated_at']
        extra_kwargs = {
            'user': {'required': False}
        }

    def create(self, validated_data):
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            validated_data['user'] = request.user
        return super().create(validated_data)