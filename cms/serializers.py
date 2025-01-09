from rest_framework import serializers
from .models import User, Content, Feedback
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from .models import User, Content, Feedback
from django.contrib.auth import authenticate



class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'role', 'managed_by']
        read_only_fields = ['role']

class UserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
    password_confirm = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password_confirm', 'role', 'managed_by')
        extra_kwargs = {
            'managed_by': {'required': False},
            'role': {'required': True}
        }

    def validate(self, attrs):
        if attrs['password'] != attrs['password_confirm']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})
        
        # Validate role and managed_by relationship
        role = attrs.get('role')
        managed_by = attrs.get('managed_by')
        
        # if role == User.CONTENT_WRITER and not managed_by:
        #     raise serializers.ValidationError({"managed_by": "Content writers must have a managing admin."})
        
        if role == User.ADMIN and managed_by:
            raise serializers.ValidationError({"managed_by": "Admin users cannot have a manager."})

        return attrs

    def create(self, validated_data):
        validated_data.pop('password_confirm')
        user = User.objects.create_user(**validated_data)
        return user

class WriterListSerializer(serializers.ModelSerializer):
    assigned_contents_count = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'managed_by', 'assigned_contents_count')

    def get_assigned_contents_count(self, obj):
        return obj.assigned_contents.count()

class ContentSerializer(serializers.ModelSerializer):
    feedbacks = serializers.SerializerMethodField()

    class Meta:
        model = Content
        fields = ['id', 'title', 'content', 'status', 'writter', 'manager', 
                 'created_at', 'updated_at', 'approved_at', 'feedbacks']
        read_only_fields = ['manager', 'approved_at']

    def get_feedbacks(self, obj):
        return FeedbackSerializer(obj.feedbacks.all(), many=True).data

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = ['id', 'content', 'comment', 'manager', 'created_at']
        read_only_fields = ['manager']





class LoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            user = authenticate(username=username, password=password)
            if user:
                if not user.is_active:
                    raise serializers.ValidationError("User is deactivated.")
                data['user'] = user
            else:
                raise serializers.ValidationError("Unable to log in with provided credentials.")
        else:
            raise serializers.ValidationError("Must include 'username' and 'password'.")

        return data