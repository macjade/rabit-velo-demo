from django.shortcuts import render, redirect
from django.contrib.auth import logout, login, authenticate
from django.views import generic
from account.models import UserProfile
# Create your views here.

import base64

class HomeView(generic.View):

    def get(self, request):
        if request.user.is_authenticated:
            return redirect('scanpage:home')

        return render(request, 'home/index.html')

class VerifyUserId(generic.View):

    def get(self, request, **kwargs):
        get_id = kwargs.get('id')

        if UserProfile.objects.filter(myid=get_id).exists():
            if request.user.is_authenticated:
                logout(request)

            userprofile = UserProfile.objects.get(myid=get_id)
            username = userprofile.user.username
            password = base64.b64decode(str(userprofile.temppass).encode()).decode()

            user = authenticate(username=username, password=password)
            request.session.set_expiry(0)

            login(self.request, user)
            return redirect('scanpage:home')

        else:
            return redirect('home:home')