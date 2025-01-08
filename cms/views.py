# from django.shortcuts import render

# # Create your views here.
# from rest_framework import viewsets, status, filters
# from rest_framework.decorators import action
# from rest_framework.response import Response
# from rest_framework.permissions import IsAuthenticated
# # from django_filters.rest_framework import DjangoFilterBackend
# from .models import Content, Feedback
# from .serializers import ContentSerializer, FeedbackSerializer, UserSerializer
# from .permissions import IsAdmin, IsContentWriter, IsManagerOrWriter

# class ContentViewSet(viewsets.ModelViewSet):
#     serializer_class = ContentSerializer
#     permission_classes = [IsAuthenticated, IsManagerOrWriter]
#     filter_backends = [ filters.SearchFilter, filters.OrderingFilter]
#     filterset_fields = ['status', 'writer', 'manager']
#     search_fields = ['title', 'content']
#     ordering_fields = ['created_at', 'updated_at', 'due_date']

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_admin():
#             return Content.objects.filter(manager=user)
#         return Content.objects.filter(writer=user)

#     @action(detail=True, methods=['post'])
#     def submit_for_review(self, request, pk=None):
#         content = self.get_object()
#         try:
#             content.submit_for_review()
#             return Response({'status': 'submitted for review'})
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdmin])
#     def approve(self, request, pk=None):
#         content = self.get_object()
#         try:
#             content.approve(request.user)
#             return Response({'status': 'approved'})
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

#     @action(detail=True, methods=['post'], permission_classes=[IsAuthenticated, IsAdmin])
#     def reject(self, request, pk=None):
#         content = self.get_object()
#         feedback_text = request.data.get('feedback')
#         if not feedback_text:
#             return Response(
#                 {'error': 'Feedback is required for rejection'},
#                 status=status.HTTP_400_BAD_REQUEST
#             )
#         try:
#             content.reject(request.user, feedback_text)
#             return Response({'status': 'rejected'})
#         except Exception as e:
#             return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

# class FeedbackViewSet(viewsets.ModelViewSet):
#     serializer_class = FeedbackSerializer
#     permission_classes = [IsAuthenticated, IsManagerOrWriter]
#     filter_backends = [ filters.OrderingFilter]
#     filterset_fields = ['content', 'resolved']
#     ordering_fields = ['created_at']

#     def get_queryset(self):
#         user = self.request.user
#         if user.is_admin():
#             return Feedback.objects.filter(manager=user)
#         return Feedback.objects.filter(content__writer=user)

#     @action(detail=True, methods=['post'])
#     def resolve(self, request, pk=None):
#         feedback = self.get_object()
#         feedback.mark_resolved()
#         return Response({'status': 'resolved'})