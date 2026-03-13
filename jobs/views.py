from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from core.permissions import HasProfile, IsClient, IsJobOwner
from .models import Category, Job
from .serializers import (
    CategorySerializer,
    JobCreateSerializer,
    JobDetailSerializer,
    JobListSerializer,
)


class CategoryListCreateView(generics.ListCreateAPIView):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.request.method == 'POST':
            return [permissions.IsAuthenticated(), HasProfile(), IsClient()]
        return [permissions.AllowAny()]


class JobListView(generics.ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        qs = Job.objects.select_related('client__user', 'category').all()
        cat = self.request.query_params.get('category')
        if cat:
            qs = qs.filter(category__slug=cat)
        skills = self.request.query_params.get('skills')
        if skills:
            for skill in skills.split(','):
                qs = qs.filter(skills_required__contains=[skill.strip()])
        status_filter = self.request.query_params.get('status')
        if status_filter:
            qs = qs.filter(status=status_filter)
        return qs


class JobCreateView(generics.CreateAPIView):
    serializer_class = JobCreateSerializer
    permission_classes = [permissions.IsAuthenticated, HasProfile, IsClient]


class JobDetailView(generics.RetrieveUpdateAPIView):
    serializer_class = JobDetailSerializer
    queryset = Job.objects.select_related('client__user', 'category')
    permission_classes = [permissions.AllowAny]

    def get_permissions(self):
        if self.request.method in ('PATCH', 'PUT'):
            return [permissions.IsAuthenticated(), HasProfile(), IsJobOwner()]
        return super().get_permissions()

    def check_object_permissions(self, request, obj):
        super().check_object_permissions(request, obj)


class JobCloseView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasProfile]

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        if job.client != request.user.profile:
            return Response(
                {'detail': 'Not the job owner.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        if job.status == 'closed':
            return Response(
                {'detail': 'Job is already closed.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        job.status = 'closed'
        job.save()
        return Response({'detail': 'Job closed.'})


class JobCompleteView(APIView):
    permission_classes = [permissions.IsAuthenticated, HasProfile]

    def post(self, request, pk):
        job = get_object_or_404(Job, pk=pk)
        if job.client != request.user.profile:
            return Response(
                {'detail': 'Not the job owner.'},
                status=status.HTTP_403_FORBIDDEN,
            )
        if job.status != 'in_progress':
            return Response(
                {'detail': 'Only in-progress jobs can be completed.'},
                status=status.HTTP_400_BAD_REQUEST,
            )
        job.status = 'completed'
        job.save()
        return Response({'detail': 'Job completed.'})


class MyJobsView(generics.ListAPIView):
    serializer_class = JobListSerializer
    permission_classes = [permissions.IsAuthenticated, HasProfile]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return Job.objects.none()
        profile = self.request.user.profile
        if profile.role == 'client':
            return Job.objects.filter(client=profile)
        return Job.objects.filter(assigned_freelancer=profile)
