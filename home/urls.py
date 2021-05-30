from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('me/<id>/', views.VerifyUserId.as_view(), name='userid'),
]