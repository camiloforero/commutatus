from django.urls import path

from . import views

urlpatterns = [
    path('', views.FilterOpportunities.as_view(), name='filter_opportunities'),
]
