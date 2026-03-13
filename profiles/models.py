from django.conf import settings
from django.db import models
from core.validators import validate_file_size, validate_image_type


class Profile(models.Model):
    ROLE_CHOICES = [
        ('freelancer', 'Freelancer'),
        ('client', 'Client'),
    ]

    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name='profile',
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)
    bio = models.TextField(blank=True, default='')
    avatar = models.ImageField(
        upload_to='avatars/',
        blank=True,
        null=True,
        validators=[validate_file_size, validate_image_type],
    )
    phone = models.CharField(max_length=20, blank=True, default='')
    location = models.CharField(max_length=100, blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'{self.user.email} ({self.role})'


class FreelancerProfile(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='freelancer_profile',
    )
    title = models.CharField(max_length=200, blank=True, default='')
    skills = models.JSONField(default=list, blank=True)
    hourly_rate = models.DecimalField(
        max_digits=10, decimal_places=2, null=True, blank=True,
    )
    portfolio_url = models.URLField(blank=True, default='')
    availability = models.BooleanField(default=True)

    def __str__(self):
        return f'Freelancer: {self.profile.user.email}'


class ClientProfile(models.Model):
    profile = models.OneToOneField(
        Profile,
        on_delete=models.CASCADE,
        related_name='client_profile',
    )
    company_name = models.CharField(max_length=200, blank=True, default='')
    company_website = models.URLField(blank=True, default='')
    industry = models.CharField(max_length=100, blank=True, default='')

    def __str__(self):
        return f'Client: {self.profile.user.email}'


class PortfolioItem(models.Model):
    freelancer_profile = models.ForeignKey(
        FreelancerProfile,
        on_delete=models.CASCADE,
        related_name='portfolio_items',
    )
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default='')
    image = models.ImageField(
        upload_to='portfolio/',
        blank=True,
        null=True,
        validators=[validate_file_size, validate_image_type],
    )
    project_url = models.URLField(blank=True, default='')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title
