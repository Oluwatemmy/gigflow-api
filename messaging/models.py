from django.db import models
from core.validators import validate_file_size


class Conversation(models.Model):
    job = models.OneToOneField(
        'jobs.Job',
        on_delete=models.CASCADE,
        related_name='conversation',
    )
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'Conversation for {self.job.title}'


class Message(models.Model):
    conversation = models.ForeignKey(
        Conversation,
        on_delete=models.CASCADE,
        related_name='messages',
    )
    sender = models.ForeignKey(
        'profiles.Profile',
        on_delete=models.CASCADE,
        related_name='sent_messages',
    )
    content = models.TextField()
    attachment = models.FileField(
        upload_to='message_attachments/',
        blank=True,
        null=True,
        validators=[validate_file_size],
    )
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'Message from {self.sender} in {self.conversation}'
