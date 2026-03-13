from rest_framework import generics, permissions, serializers as drf_serializers, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from core.permissions import HasProfile, IsClient, IsFreelancer, IsJobOwner, IsProposalAuthor
from jobs.models import Job
from messaging.models import Conversation
from .models import Proposal
from .serializers import ProposalSerializer, ProposalCreateSerializer


class ProposalListView(generics.ListAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated, HasProfile]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Proposal.objects.none()
        job = get_object_or_404(Job, pk=self.kwargs['job_id'])
        if job.client != self.request.user.profile:
            return Proposal.objects.none()
        return Proposal.objects.filter(job=job).select_related('freelancer__user')


class ProposalCreateView(generics.CreateAPIView):
    serializer_class = ProposalCreateSerializer
    permission_classes = [permissions.IsAuthenticated, HasProfile, IsFreelancer]

    def perform_create(self, serializer):
        job = get_object_or_404(Job, pk=self.kwargs['job_id'])
        if job.status != 'open':
            raise drf_serializers.ValidationError('Can only submit proposals to open jobs.')
        if Proposal.objects.filter(job=job, freelancer=self.request.user.profile).exists():
            raise drf_serializers.ValidationError('You have already submitted a proposal for this job.')
        serializer.save(job=job, freelancer=self.request.user.profile)


class ProposalDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated, HasProfile]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Proposal.objects.none()
        return Proposal.objects.filter(job_id=self.kwargs['job_id'])

    def check_object_permissions(self, request, obj):
        profile = request.user.profile
        is_owner = obj.job.client == profile
        is_author = obj.freelancer == profile
        if not (is_owner or is_author):
            self.permission_denied(request)
        if request.method in ('PATCH', 'PUT', 'DELETE'):
            if not is_author:
                self.permission_denied(request)
            if request.method in ('PATCH', 'PUT') and obj.status != 'pending':
                self.permission_denied(request, message='Can only edit pending proposals.')


class ProposalAcceptView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasProfile]

    def post(self, request, job_id, pk):
        job = get_object_or_404(Job, pk=job_id)
        if job.client != request.user.profile:
            return Response(
                {'detail': 'Not the job owner.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        if job.status != 'open':
            return Response(
                {'detail': 'Job is not open.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        proposal = get_object_or_404(Proposal, pk=pk, job=job)
        if proposal.status != 'pending':
            return Response(
                {'detail': 'Proposal is not pending.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        proposal.status = 'accepted'
        proposal.save()

        # Reject other pending proposals
        Proposal.objects.filter(job=job, status='pending').exclude(pk=pk).update(
            status='rejected',
        )

        # Update job
        job.status = 'in_progress'
        job.assigned_freelancer = proposal.freelancer
        job.save()

        # Create conversation
        Conversation.objects.get_or_create(job=job)

        return Response({'detail': 'Proposal accepted.'})


class ProposalRejectView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasProfile]

    def post(self, request, job_id, pk):
        job = get_object_or_404(Job, pk=job_id)
        if job.client != request.user.profile:
            return Response(
                {'detail': 'Not the job owner.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        proposal = get_object_or_404(Proposal, pk=pk, job=job)
        if proposal.status != 'pending':
            return Response(
                {'detail': 'Proposal is not pending.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        proposal.status = 'rejected'
        proposal.save()
        return Response({'detail': 'Proposal rejected.'})


class MyProposalsView(generics.ListAPIView):
    serializer_class = ProposalSerializer
    permission_classes = [permissions.IsAuthenticated, HasProfile, IsFreelancer]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Proposal.objects.none()
        return Proposal.objects.filter(
            freelancer=self.request.user.profile,
        ).select_related('job', 'freelancer__user')
