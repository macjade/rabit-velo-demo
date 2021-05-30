from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, BaseUserManager
from django.utils import timezone

import random
import base64
# Create your models here.

class PwaManager(BaseUserManager):

    def create_user(self, username, email, password=None, is_active=True, is_staff=False, is_admin=False):
        if not username:
            raise ValueError("User must have a username")

        if not email:
            raise ValueError("User must have an email address")

        if not password:
            raise ValueError("User must have a password")

        user_obj = self.model(
            username=username,
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)

        return user_obj

    def create_staffuser(self, username, email, password=None):

        user_staff = self.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True
        )

        return user_staff

    def create_superuser(self, username, email, password=None):

        user_admin = self.create_user(
            username=username,
            email=email,
            password=password,
            is_staff=True,
            is_admin=True
        )

        return user_admin

class Pwa(AbstractBaseUser, PermissionsMixin):

    firstname = models.CharField(max_length=30)
    lastname = models.CharField(max_length=30)
    username = models.CharField(max_length=50, unique=True)
    email = models.EmailField(max_length=255, unique=True)
    active = models.BooleanField(default=True)
    is_blocked = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    admin = models.BooleanField(default=False)
    date_of_joining = models.DateTimeField(default=timezone.now)

    USERNAME_FIELD = 'email'

    REQUIRED_FIELDS = ['username']

    objects = PwaManager()

    def __str__(self):
        return str(self.get_full_name()) + " - " + str(self.email)

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    def get_full_name(self):
        return str(self.firstname).capitalize() + " " + str(self.lastname).capitalize()

    def get_short_name(self):
        return str(self.firstname).capitalize() + " " + str(self.lastname).capitalize()

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_active(self):
        return self.active

    def createnewuser(self, firstname, lastname, email, dob, password):

        new_user = self
        check_user = self.find_user(email)
        try:
            if not check_user:
                new_user.firstname = firstname
                new_user.lastname = lastname
                new_user.username = firstname+lastname
                new_user.email = email
                new_user.set_password(password)
                new_user.client = True
                new_user.save()

                myid = self.generate_userprofile_id()
                temppass = self.encode_pass(password)
                UserProfile().createprofile(new_user.pk, dob, myid, temppass)

                return {'status':True}
            else:
                return {'status':False, 'message':'User already exists'}
        except:
            return {'status':False, 'message':'Unable to complete registeration at the moment'}

    def encode_pass(self, password):
        encode_str = str(password).encode()
        return base64.b64encode(encode_str).decode()

    def generate_userprofile_id(self):
        sequence = '1234567890XAZBDE'
        id = ''.join(random.choice(sequence) for i in range(0, 6))
        check_id = UserProfile.objects.filter(myid=id).exists()

        if check_id:
            return self.generate_userprofile_id()
        else:
            return id

    def find_user(self, email=None):

        find_user = self.__class__
        check_user = find_user.objects.filter(email=email)
        if check_user:
            return check_user
        else:
            return False

class UserProfile(models.Model):

    SCANNED_CHOICE = {
        ('None', 'None'),
        ('First', 'First'),
        ('Second', 'Second'),
    }

    user = models.ForeignKey(Pwa, on_delete=models.CASCADE)
    scanned_times = models.CharField(max_length=10, default='None', choices=SCANNED_CHOICE)
    myid = models.CharField(max_length=100, default="", unique=True)
    temppass = models.CharField(max_length=255, default="")
    dob = models.DateField(default=timezone.now)

    def __str__(self):
        return str(self.user.get_full_name()) + ' ' + str(self.scanned_times)

    def createprofile(self, id, dob, myid, tempass):
        newprofile = self
        newprofile.user = Pwa.objects.get(pk=id)
        newprofile.myid = myid
        newprofile.dob = dob
        newprofile.temppass = tempass
        newprofile.save()

        return True

    def editprofile(self, id):
        tracker = ['None', 'First', 'Second']
        editprofile = self.__class__.objects.get(pk=id)
        if editprofile.scanned_times in tracker:
            if tracker.index(editprofile.scanned_times) + 1 < len(tracker):
                updated_scan = tracker[tracker.index(editprofile.scanned_times) + 1]
            else:
                updated_scan = tracker[-1]
            editprofile.scanned_times = updated_scan
        editprofile.save()

        return editprofile