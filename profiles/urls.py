from django.urls import path
from . import views

app_name = 'profiles'

urlpatterns = [
    path('', views.ProfileCreateView.as_view(), name='create'),
    path('me/', views.ProfileMeView.as_view(), name='me'),
    path('me/portfolio/', views.PortfolioCreateView.as_view(), name='portfolio-create'),
    path('me/portfolio/<int:pk>/', views.PortfolioDeleteView.as_view(), name='portfolio-delete'),
    path('freelancers/', views.FreelancerListView.as_view(), name='freelancer-list'),
    path('<int:pk>/', views.ProfileDetailView.as_view(), name='detail'),
]
