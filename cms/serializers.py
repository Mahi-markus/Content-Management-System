# from rest_framework import serializers
# from django.contrib.auth import get_user_model
# from .models import Content, Feedback

# User = get_user_model()

# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'email', 'first_name', 'last_name', 'role', 'managed_by']
#         read_only_fields = ['id']

# class ContentSerializer(serializers.ModelSerializer):
#     writer_name = serializers.CharField(source='writer.get_full_name', read_only=True)
#     manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)
#     feedbacks = serializers.SerializerMethodField()

#     class Meta:
#         model = Content
#         fields = [
#             'id', 'title', 'content', 'status', 'writer', 'writer_name',
#             'manager', 'manager_name', 'created_at', 'updated_at',
#             'approved_at', 'due_date', 'is_editable', 'feedbacks'
#         ]
#         read_only_fields = ['id', 'created_at', 'updated_at', 'approved_at', 'is_editable']

#     def get_feedbacks(self, obj):
#         return FeedbackSerializer(obj.feedbacks.all(), many=True).data

# class FeedbackSerializer(serializers.ModelSerializer):
#     manager_name = serializers.CharField(source='manager.get_full_name', read_only=True)

#     class Meta:
#         model = Feedback
#         fields = [
#             'id', 'content', 'comment', 'manager', 'manager_name',
#             'created_at', 'resolved', 'resolved_at'
#         ]
#         read_only_fields = ['id', 'created_at', 'resolved_at']