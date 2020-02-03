from django.contrib import admin

from . models import VineAlbum,Vine,Profile
# Register your models here.

admin.site.register(VineAlbum)
admin.site.register(Vine)
admin.site.register(Profile)