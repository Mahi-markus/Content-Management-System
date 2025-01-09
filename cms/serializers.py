from rest_framework import serializers
from .models import User, Content, Feedback

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'role')

class ContentSerializer(serializers.ModelSerializer):
    writter = serializers.StringRelatedField()
    manager = serializers.StringRelatedField()

    class Meta:
        model = Content
        fields = ('id', 'title', 'content', 'status', 'writter', 'manager', 'created_at', 'updated_at', 'approved_at')

class FeedbackSerializer(serializers.ModelSerializer):
    content = serializers.StringRelatedField()
    manager = serializers.StringRelatedField()

    class Meta:
        model = Feedback
        fields = ('id', 'content', 'manager', 'comment')