from django.urls import path
from . import views

app_name = 'scanpage'

urlpatterns = [
    path('', views.HomeView.as_view(), name='home'),
    path('scanned/<id>/', views.VerifyUserScan.as_view(), name='scanned_user'),
    path('redirect/<id>/', views.DynamicRedirect.as_view(), name='redirect_user'),
    path('generateqrcode/', views.GenerateQrView.as_view(), name='generate_code'),
]