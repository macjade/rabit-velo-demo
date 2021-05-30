from django.urls import path
from . import views

app_name = 'account'

urlpatterns = [
    path('registeration/', views.HomeView.as_view(), name='register'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('logout/', views.logoutview, name="logout"),
]