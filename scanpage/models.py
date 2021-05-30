from django.db import models

# Create your models here.

class QrCode(models.Model):

    secret_key = models.CharField(max_length=255, default="", unique=True)
    image_obj = models.CharField(max_length=3000, default="")

    def __str__(self):
        return self.secret_key

    def newQrCode(self, secret, image):

        newQR = self
        newQR.secret_key = secret
        newQR.image_obj = image
        newQR.save()

        return newQR

class DynamicString(models.Model):

    code = models.ForeignKey(QrCode, on_delete=models.CASCADE)
    key = models.CharField(max_length=255, default="")

    def __str__(self):
        return str(self.code.secret_key) + ' - '+ str(self.key)

    def adddynamicstring(self, code, key):
        newString = self
        newString.code = QrCode.objects.get(secret_key=code)
        newString.key = key
        newString.save()
        return newString