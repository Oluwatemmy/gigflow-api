from django.urls import path
from . import views

app_name = 'jobs'

urlpatterns = [
    path('', views.JobListView.as_view(), name='list'),
    path('my/', views.MyJobsView.as_view(), name='my-jobs'),
    path('create/', views.JobCreateView.as_view(), name='create'),
    path('<int:pk>/', views.JobDetailView.as_view(), name='detail'),
    path('<int:pk>/close/', views.JobCloseView.as_view(), name='close'),
    path('<int:pk>/complete/', views.JobCompleteView.as_view(), name='complete'),
]
