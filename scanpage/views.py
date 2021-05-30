from django.shortcuts import render, redirect
from django.views import generic
from django.http import JsonResponse
from .models import QrCode, DynamicString
from account.models import UserProfile

import uuid
import qrcode
import base64
# Create your views here.

class HomeView(generic.View):

    def get(self, request):
        context = {}

        if not request.user.is_authenticated:
            return redirect('home:home')

        if request.session.get('msg_register'):
            context['new_user'] = True
            request.session.pop('msg_register')

        if request.session.get('msg_error'):
            context['msg_error'] = request.session.get('msg_error')
            request.session.pop('msg_error')

        return render(request, 'scanpage/scanpage.html', context)

class DynamicRedirect(generic.View):

    def get(self, request, **kwargs):

        get_id = str(kwargs.get('id'))
        if DynamicString.objects.filter(key=get_id).exists():
            DynamicString.objects.filter(key=get_id).delete()
            tracker = request.user.userprofile_set.get().scanned_times
            if tracker == 'First':
                return render(request, 'scanpage/first_timer.html')
            else:
                return render(request, 'scanpage/existing_timer.html')
        else:
            request.session['msg_error'] = 'Scan ID is either invalid or as expired, please scan again'
            return redirect('scanpage:home')

class VerifyUserScan(generic.View):

    def get(self, request, **kwargs):
        context={}
        get_id = str(kwargs.get('id')).replace('__', '/')

        if QrCode.objects.filter(secret_key=get_id).exists():
            newstring = DynamicString().adddynamicstring(get_id, str(uuid.uuid4()))
            edittracker = UserProfile().editprofile(request.user.userprofile_set.get().pk)
            context['status'] = True
            context['url'] = '/scanner/redirect/'+newstring.key+'/'
        else:
            context['status'] = False
            context['message'] = 'Only BAT registered QR Codes are allowed'

        return JsonResponse(context)

class GenerateQrView(generic.View):

    def generatesecret(self):
        secret = str(uuid.uuid4())
        if QrCode.objects.filter(secret_key=secret).exists():
            return self.generatesecret()
        return secret

    def get(self, request):
        get_secret = self.generatesecret()

        qr = qrcode.QRCode(
            version=1,
            box_size=15,
            border=3,
        )

        qr.add_data(get_secret)
        qr.make(fit=True)
        img = qr.make_image(fill="black", back_color='white')
        img.save('temp_'+get_secret+'.png')
        with open('temp_'+get_secret+'.png', "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read())

        newqr = QrCode().newQrCode(get_secret, encoded_string.decode("utf-8"))

        barcode = newqr.image_obj

        context = {
            'barcode': barcode
        }

        return render(request, 'scanpage/generateqrcode.html', context)