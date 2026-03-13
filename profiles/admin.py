from django.contrib import admin
from .models import Profile, FreelancerProfile, ClientProfile, PortfolioItem

admin.site.register(Profile)
admin.site.register(FreelancerProfile)
admin.site.register(ClientProfile)
admin.site.register(PortfolioItem)
