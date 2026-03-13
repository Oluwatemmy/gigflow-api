from django.urls import path
from . import views

app_name = 'reviews'

urlpatterns = [
    path(
        'job/<int:job_id>/',
        views.JobReviewListView.as_view(),
        name='job-reviews',
    ),
    path(
        'job/<int:job_id>/create/',
        views.JobReviewCreateView.as_view(),
        name='job-review-create',
    ),
    path(
        'profile/<int:profile_id>/',
        views.ProfileReviewListView.as_view(),
        name='profile-reviews',
    ),
]
