from django.urls import path
from . import views

app_name = 'proposals'

urlpatterns = [
    path('my/', views.MyProposalsView.as_view(), name='my-proposals'),
    path(
        '<int:job_id>/',
        views.ProposalListView.as_view(),
        name='list',
    ),
    path(
        '<int:job_id>/create/',
        views.ProposalCreateView.as_view(),
        name='create',
    ),
    path(
        '<int:job_id>/<int:pk>/',
        views.ProposalDetailView.as_view(),
        name='detail',
    ),
    path(
        '<int:job_id>/<int:pk>/accept/',
        views.ProposalAcceptView.as_view(),
        name='accept',
    ),
    path(
        '<int:job_id>/<int:pk>/reject/',
        views.ProposalRejectView.as_view(),
        name='reject',
    ),
]
