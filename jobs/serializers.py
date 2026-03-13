from rest_framework import serializers
from .models import Category, Job, JobAttachment


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'slug', 'description']
        read_only_fields = ['slug']

    def validate_name(self, value):
        from django.utils.text import slugify
        slug = slugify(value)
        if Category.objects.filter(slug=slug).exists():
            raise serializers.ValidationError('A category with this name already exists.')
        return value

    def create(self, validated_data):
        from django.utils.text import slugify
        validated_data['slug'] = slugify(validated_data['name'])
        return super().create(validated_data)


class JobAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobAttachment
        fields = ['id', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class JobListSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.user.email', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    skills_required = serializers.ListField(child=serializers.CharField(), required=False)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'client_name', 'category', 'category_name',
            'skills_required', 'budget_type', 'budget_min', 'budget_max',
            'status', 'deadline', 'created_at',
        ]


class JobDetailSerializer(serializers.ModelSerializer):
    client_name = serializers.CharField(source='client.user.email', read_only=True)
    category_name = serializers.CharField(source='category.name', read_only=True)
    skills_required = serializers.ListField(child=serializers.CharField(), required=False)
    attachments = JobAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'client', 'client_name',
            'category', 'category_name', 'skills_required',
            'budget_type', 'budget_min', 'budget_max', 'status',
            'assigned_freelancer', 'deadline', 'attachments',
            'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'client', 'status', 'assigned_freelancer', 'created_at', 'updated_at']


class JobCreateSerializer(serializers.ModelSerializer):
    skills_required = serializers.ListField(
        child=serializers.CharField(), required=False, default=list,
    )

    class Meta:
        model = Job
        fields = [
            'id', 'title', 'description', 'category', 'skills_required',
            'budget_type', 'budget_min', 'budget_max', 'deadline',
        ]
        read_only_fields = ['id']

    def validate(self, data):
        if data['budget_min'] > data['budget_max']:
            raise serializers.ValidationError('budget_min cannot exceed budget_max.')
        return data

    def create(self, validated_data):
        validated_data['client'] = self.context['request'].user.profile
        return super().create(validated_data)
