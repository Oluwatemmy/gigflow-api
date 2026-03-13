from rest_framework import serializers
from .models import Proposal, ProposalAttachment


class ProposalAttachmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProposalAttachment
        fields = ['id', 'file', 'uploaded_at']
        read_only_fields = ['id', 'uploaded_at']


class ProposalSerializer(serializers.ModelSerializer):
    freelancer_email = serializers.CharField(
        source='freelancer.user.email', read_only=True,
    )
    attachments = ProposalAttachmentSerializer(many=True, read_only=True)

    class Meta:
        model = Proposal
        fields = [
            'id', 'job', 'freelancer', 'freelancer_email',
            'cover_letter', 'proposed_rate', 'estimated_duration_days',
            'status', 'attachments', 'created_at', 'updated_at',
        ]
        read_only_fields = ['id', 'job', 'freelancer', 'status', 'created_at', 'updated_at']


class ProposalCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Proposal
        fields = [
            'id', 'cover_letter', 'proposed_rate', 'estimated_duration_days',
        ]
        read_only_fields = ['id']
