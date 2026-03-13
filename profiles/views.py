from rest_framework import generics, permissions, status
from rest_framework.response import Response
from core.permissions import HasProfile, IsFreelancer
from .models import Profile, PortfolioItem
from .serializers import (
    ProfileCreateSerializer,
    ProfileSerializer,
    PortfolioItemSerializer,
)


class ProfileCreateView(generics.CreateAPIView):
    serializer_class = ProfileCreateSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProfileMeView(generics.RetrieveUpdateAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.IsAuthenticated, HasProfile]

    def get_object(self):
        return self.request.user.profile


class ProfileDetailView(generics.RetrieveAPIView):
    serializer_class = ProfileSerializer
    queryset = Profile.objects.all()
    permission_classes = [permissions.AllowAny]


class FreelancerListView(generics.ListAPIView):
    serializer_class = ProfileSerializer
    permission_classes = [permissions.AllowAny]

    def get_queryset(self):
        return Profile.objects.filter(role='freelancer').select_related(
            'user', 'freelancer_profile',
        )


class PortfolioCreateView(generics.CreateAPIView):
    serializer_class = PortfolioItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsFreelancer]

    def perform_create(self, serializer):
        serializer.save(
            freelancer_profile=self.request.user.profile.freelancer_profile,
        )


class PortfolioDeleteView(generics.DestroyAPIView):
    serializer_class = PortfolioItemSerializer
    permission_classes = [permissions.IsAuthenticated, IsFreelancer]

    def get_queryset(self):
        if getattr(self, 'swagger_fake_view', False):
            return PortfolioItem.objects.none()
        return PortfolioItem.objects.filter(
            freelancer_profile=self.request.user.profile.freelancer_profile,
        )
