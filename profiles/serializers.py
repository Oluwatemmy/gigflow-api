from rest_framework import serializers
from .models import Profile, FreelancerProfile, ClientProfile, PortfolioItem


class FreelancerProfileSerializer(serializers.ModelSerializer):
    skills = serializers.ListField(child=serializers.CharField(), required=False, default=list)

    class Meta:
        model = FreelancerProfile
        fields = ['title', 'skills', 'hourly_rate', 'portfolio_url', 'availability']


class ClientProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ClientProfile
        fields = ['company_name', 'company_website', 'industry']


class PortfolioItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = PortfolioItem
        fields = ['id', 'title', 'description', 'image', 'project_url', 'created_at']
        read_only_fields = ['id', 'created_at']


class ProfileCreateSerializer(serializers.ModelSerializer):
    freelancer_profile = FreelancerProfileSerializer(required=False)
    client_profile = ClientProfileSerializer(required=False)

    class Meta:
        model = Profile
        fields = [
            'id', 'role', 'bio', 'avatar', 'phone', 'location',
            'freelancer_profile', 'client_profile', 'created_at',
        ]
        read_only_fields = ['id', 'created_at']

    def validate(self, data):
        if Profile.objects.filter(user=self.context['request'].user).exists():
            raise serializers.ValidationError('You already have a profile.')
        role = data.get('role')
        if role == 'freelancer' and 'client_profile' in data:
            raise serializers.ValidationError('Freelancer cannot include client_profile data.')
        if role == 'client' and 'freelancer_profile' in data:
            raise serializers.ValidationError('Client cannot include freelancer_profile data.')
        return data

    def create(self, validated_data):
        freelancer_data = validated_data.pop('freelancer_profile', None)
        client_data = validated_data.pop('client_profile', None)
        validated_data['user'] = self.context['request'].user
        profile = Profile.objects.create(**validated_data)

        if profile.role == 'freelancer':
            FreelancerProfile.objects.create(
                profile=profile, **(freelancer_data or {})
            )
        elif profile.role == 'client':
            ClientProfile.objects.create(
                profile=profile, **(client_data or {})
            )
        return profile


class ProfileSerializer(serializers.ModelSerializer):
    freelancer_profile = FreelancerProfileSerializer(required=False)
    client_profile = ClientProfileSerializer(required=False)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = [
            'id', 'email', 'role', 'bio', 'avatar', 'phone', 'location',
            'freelancer_profile', 'client_profile', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'role', 'created_at', 'updated_at']

    def update(self, instance, validated_data):
        freelancer_data = validated_data.pop('freelancer_profile', None)
        client_data = validated_data.pop('client_profile', None)

        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if freelancer_data and hasattr(instance, 'freelancer_profile'):
            for attr, value in freelancer_data.items():
                setattr(instance.freelancer_profile, attr, value)
            instance.freelancer_profile.save()

        if client_data and hasattr(instance, 'client_profile'):
            for attr, value in client_data.items():
                setattr(instance.client_profile, attr, value)
            instance.client_profile.save()

        return instance
