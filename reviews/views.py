from rest_framework import generics, permissions, serializers, status
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from core.permissions import HasProfile
from jobs.models import Job
from .models import Review
from .serializers import ReviewSerializer


class JobReviewCreateView(generics.CreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.IsAuthenticated, HasProfile]

    def perform_create(self, serializer):
        job = get_object_or_404(Job, pk=self.kwargs['job_id'])
        profile = self.request.user.profile

        if job.status != 'completed':
            raise serializers.ValidationError('Job must be completed to leave a review.')

        if not job.assigned_freelancer:
            raise serializers.ValidationError('Job does not have an assigned freelancer.')

        is_client = job.client == profile
        is_freelancer = job.assigned_freelancer == profile
        if not (is_client or is_freelancer):
            raise serializers.ValidationError('You are not a participant in this job.')

        reviewee = job.assigned_freelancer if is_client else job.client

        serializer.save(job=job, reviewer=profile, reviewee=reviewee)


class JobReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        return Review.objects.filter(job_id=self.kwargs['job_id']).select_related(
            'reviewer__user', 'reviewee__user',
        )


class ProfileReviewListView(generics.ListAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Review.objects.none()
        return Review.objects.filter(reviewee_id=self.kwargs['profile_id']).select_related(
            'reviewer__user', 'reviewee__user',
        )
