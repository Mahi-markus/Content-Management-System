from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from django.core.exceptions import ValidationError


class User(AbstractUser):
    ADMIN = 'admin'
    CONTENT_WRITER = 'writer'

    ROLE_CHOICES = [
        (ADMIN, 'Admin'),
        (CONTENT_WRITER, 'Content Writer'),
    ]

    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default=CONTENT_WRITER)
    managed_by = models.ForeignKey(
        'self',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='writers',
        limit_choices_to={'role': ADMIN}
    )

    def is_admin(self):
        return self.role == self.ADMIN

    def is_content_writer(self):
        return self.role == self.CONTENT_WRITER

    def save(self, *args, **kwargs):
        if self.role == self.ADMIN and self.managed_by is not None:
            raise ValidationError("Admin users cannot be managed by other users")

        if self.managed_by and not self.managed_by.is_admin():
            raise ValidationError("Writers can only be managed by admin users")
        super().save(*args, **kwargs)

    def get_managed_writers(self):
        """Get all writers managed by this admin"""
        if not self.is_admin():
            return User.objects.none()
        return self.writers.all()


class Content(models.Model):
    ASSIGNED = 'assigned'
    IN_PROGRESS = 'in_progress'
    PENDING_REVIEW = 'pending_review'
    APPROVED = 'approved'

    STATUS_CHOICES = [
        (ASSIGNED, 'Assigned'),
        (IN_PROGRESS, 'In Progress'),
        (PENDING_REVIEW, 'Pending Review'),
        (APPROVED, 'Approved'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default=ASSIGNED)
    writter = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_contents',
        limit_choices_to={'role': User.CONTENT_WRITER}
    )
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='assigned_by_contents',
        limit_choices_to={'role': User.ADMIN}
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    approved_at = models.DateTimeField(null=True, blank=True)

    def clean(self):
        # Ensure the assigned writer is managed by the assigning admin
        if self.writter and self.manager:
            if self.writter.managed_by != self.manager:
                raise ValidationError(
                    "Content can only be assigned to writers managed by the assigning admin"
                )

    def approve(self):
        self.status = self.APPROVED
        self.approved_at = timezone.now()
        self.save()

    class Meta:
        ordering = ['-created_at']


class Feedback(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='feedbacks')
    comment = models.TextField()
    manager = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        limit_choices_to={'role': User.ADMIN}
    )
    created_at = models.DateTimeField(auto_now_add=True)  # Renamed from `writer`

    def clean(self):
        # Ensure feedback is only created by the admin managing the content's writer
        if self.content.writter.managed_by != self.manager:
            raise ValidationError(
                "Feedback can only be provided by the admin managing the content writer"
            )

    class Meta:
        ordering = ['-created_at']
