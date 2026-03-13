from rest_framework.permissions import BasePermission


class HasProfile(BasePermission):
    """User has created a profile."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, 'profile')
        )


class IsClient(BasePermission):
    """User's profile role is 'client'."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, 'profile')
            and request.user.profile.role == 'client'
        )


class IsFreelancer(BasePermission):
    """User's profile role is 'freelancer'."""

    def has_permission(self, request, view):
        return (
            request.user.is_authenticated
            and hasattr(request.user, 'profile')
            and request.user.profile.role == 'freelancer'
        )


class IsJobOwner(BasePermission):
    """User is the client who posted the job."""

    def has_object_permission(self, request, view, obj):
        job = getattr(obj, 'job', obj)
        return job.client == request.user.profile


class IsProposalAuthor(BasePermission):
    """User is the freelancer who submitted the proposal."""

    def has_object_permission(self, request, view, obj):
        return obj.freelancer == request.user.profile


class IsConversationParticipant(BasePermission):
    """User is the job's client or assigned freelancer."""

    def has_object_permission(self, request, view, obj):
        conversation = getattr(obj, 'conversation', obj)
        job = conversation.job
        profile = request.user.profile
        return profile == job.client or profile == job.assigned_freelancer
