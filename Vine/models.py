from django.contrib.auth.models import User
from django.db import models
from django.db.models import CharField
from django.urls import reverse
from languages.fields import LanguageField
from django_countries.fields import CountryField
from django import template
from django_mysql.models import ListCharField


register = template.Library()

# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    about_me = models.CharField(max_length=250)

    def __str__(self):
        return self.user.username

class VineAlbum(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    artist = models.CharField(max_length=100)
    title = models.CharField(max_length=100)
    genre = models.CharField(max_length=100)
    vine_logo = models.FileField()

    def get_absolute_url(self):
        return reverse('Vine:detail', kwargs={'pk': self.pk})

    def __str__(self):
        return self.title + ' - ' + self.artist

class Vine(models.Model):
    album = models.ForeignKey(VineAlbum,on_delete=models.CASCADE)
    vine_title = models.CharField(max_length=100)
    vine_poster= models.FileField()
    video = models.FileField()
    country = CountryField(blank_label='Select Country',null=True)
    date = models.DateTimeField(auto_now_add=True)
    language = LanguageField()
    likes = ListCharField(base_field=CharField(max_length=100),max_length=(6 * 11),default=[])
    dislikes = ListCharField(base_field=CharField(max_length=100),max_length=(6 * 11),default=[])


    def __str__(self):
        return self.vine_title


    def is_liked(self,profile):
        return profile in self.likes


    def is_disliked(self,profile):
        return profile in self.dislikes


    def add_like(self,profile):
      if(self.is_liked(profile)):
        self.likes.remove(profile)
      else:
        self.likes.append(profile)
        if(self.is_disliked(profile)):
            self.dislikes.remove(profile)
      self.save()

    def add_dislike(self,profile):
        if (self.is_disliked(profile)):
            self.dislikes.remove(profile)
        else:
            self.dislikes.append(profile)
            if(self.is_liked(profile)):
                self.likes.remove(profile)
        self.save()

