from django.shortcuts import render, redirect
from django.views import generic
from django.contrib.auth import login, logout, authenticate
from .models import Pwa
# Create your views here.

class HomeView(generic.View):

    def get(self, request):

        context = {}

        if request.user.is_authenticated:
            return redirect('scanpage:home')

        if request.session.get('msg_error'):
            context['msg_error'] = request.session.get('msg_error')
            request.session.pop('msg_error')

        return render(request, 'account/register.html', context)

    def post(self, request):
        firstname = request.POST['fname']
        lastname = request.POST['lname']
        email = request.POST['email']
        dob = request.POST['dob']
        password = request.POST['password']

        new_user = Pwa().createnewuser(firstname, lastname, email, dob, password)
        if new_user:
            user = authenticate(username=email, password=password)

            if user is not None:
                if not user.is_blocked:
                    request.session.set_expiry(0)

                    login(self.request, user)
                    request.session['msg_register'] = 'new user'
                    return redirect('scanpage:home')
                else:
                    request.session['msg_error'] = 'Your account has been blocked for violating VELO policies'
                    return redirect('account:register')
            else:
                request.session['msg_error'] = 'Unable to complete registration at the moment'
                return redirect('account:register')
        else:
            request.session['msg_error'] = 'Unable to complete registration at the moment'
            return redirect('account:register')

class LoginView(generic.View):

    def get(self, request):
        context = {}
        if request.user.is_authenticated:
            return redirect('scanpage:home')

        if request.session.get('msg_error'):
            context['msg_error'] = request.session.get('msg_error')
            request.session.pop('msg_error')

        return render(request, 'account/login.html', context)

    def post(self, request, **kwargs):

        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(username=email, password=password)

        if user is not None:
            if not user.is_blocked:
                request.session.set_expiry(0)

                login(self.request, user)
                return redirect('scanpage:home')
            else:
                request.session['msg_error'] = 'Your account has been blocked for violating VELO policies'
                return redirect('account:login')
        else:
            request.session['msg_error'] = 'Invalid Email/Password'
            return redirect('account:login')

def logoutview(request):
    logout(request)
    return redirect("home:home")