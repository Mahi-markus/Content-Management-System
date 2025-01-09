from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserViewSet, ContentViewSet, FeedbackViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'contents', ContentViewSet, basename='content')
router.register(r'feedbacks', FeedbackViewSet, basename='feedback')

urlpatterns = [
    path('api/', include(router.urls)),
]