from rest_framework import serializers
from .models import Review


class ReviewSerializer(serializers.ModelSerializer):
    reviewer_email = serializers.CharField(source='reviewer.user.email', read_only=True)
    reviewee_email = serializers.CharField(source='reviewee.user.email', read_only=True)

    class Meta:
        model = Review
        fields = [
            'id', 'job', 'reviewer', 'reviewer_email',
            'reviewee', 'reviewee_email', 'rating', 'comment', 'created_at',
        ]
        read_only_fields = ['id', 'job', 'reviewer', 'reviewee', 'created_at']
