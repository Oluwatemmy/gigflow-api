from django.urls import path
from . import views

app_name = 'messaging'

urlpatterns = [
    path(
        'jobs/<int:job_id>/',
        views.JobMessageListCreateView.as_view(),
        name='job-messages',
    ),
    path(
        'conversations/',
        views.ConversationListView.as_view(),
        name='conversation-list',
    ),
]
