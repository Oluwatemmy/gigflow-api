from rest_framework import generics, permissions, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Q
from core.permissions import HasProfile
from jobs.models import Job
from .models import Conversation, Message
from .serializers import ConversationSerializer, MessageSerializer


class JobMessageListCreateView(generics.ListCreateAPIView):
    serializer_class = MessageSerializer
    permission_classes = [permissions.IsAuthenticated, HasProfile]

    def get_conversation(self):
        job = get_object_or_404(Job, pk=self.kwargs['job_id'])
        profile = self.request.user.profile
        if profile != job.client and profile != job.assigned_freelancer:
            self.permission_denied(self.request)
        return get_object_or_404(Conversation, job=job)

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Message.objects.none()
        conversation = self.get_conversation()
        return Message.objects.filter(conversation=conversation).select_related(
            'sender__user',
        )

    def perform_create(self, serializer):
        conversation = self.get_conversation()
        serializer.save(
            conversation=conversation,
            sender=self.request.user.profile,
        )


class ConversationListView(generics.ListAPIView):
    serializer_class = ConversationSerializer
    permission_classes = [permissions.IsAuthenticated, HasProfile]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Conversation.objects.none()
        profile = self.request.user.profile
        return Conversation.objects.filter(
            Q(job__client=profile) | Q(job__assigned_freelancer=profile),
        ).select_related('job').prefetch_related('messages')
