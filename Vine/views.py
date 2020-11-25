from datetime import timezone
from logging import log

from django.contrib.auth import authenticate,login,logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.views import generic
from django.views.generic import View
from django.shortcuts import get_object_or_404
from .forms import UserForm, Login, VineAlbum_form, Vine_form
from .models import VineAlbum, Vine, Profile
from django.db.models import Q
from django.contrib.auth.models import User
# Create your views here.
'''
class IndexView(generic.ListView):
    template_name = 'vine/base_visitor.html'
    context_object_name = 'all_albums'

    def get_queryset(self):
        return VineAlbum.objects.all()

class DetailView(generic.DetailView):
    context_object_name = 'album'
    model = VineAlbum
    template_name = 'vine/details.html'
'''

def IndexView(request):
    if not request.user.is_authenticated:
        return render(request, 'vine/base_visitor.html', {'all_albums': VineAlbum.objects.all()})
    else:
        albums = VineAlbum.objects.all()
        vines = Vine.objects.all()
        query = request.GET.get("q")
        if query:
            albums_selected = albums.filter(
                Q(artist__icontains=query) | Q(title__icontains=query) | Q(genre__icontains=query)
            ).distinct()
            vines_selected = vines.filter(
                Q(vine_title__icontains=query) | Q(country__icontains=query) | Q(language__icontains=query)
            ).distinct()
            return render(request, 'vine/index.html', {'all_albums': albums_selected,'all_vines': vines_selected})
        else:
            print(VineAlbum.objects.all())
            return render(request, 'vine/index.html', {'all_albums': VineAlbum.objects.all().reverse().reverse() })

def DetailView(request,album_id):
    if not request.user.is_authenticated:
        return render(request, 'vine/login.html')
    selected_album = get_object_or_404(VineAlbum, pk=album_id)
    return render(request, 'vine/details.html', {'album': selected_album})

def DetailView_vine(request,album_id,vine_id):
    if not request.user.is_authenticated:
        return render(request, 'vine/login.html')
    selected_vine = get_object_or_404(Vine, pk=vine_id)
    return render(request,'vine/vine_details.html',{'vine': selected_vine})

def vine_Index(request):
    if not request.user.is_authenticated:
        return render(request, 'vine/vine_index_notLoggedIn.html', {'all_vines': Vine.objects.all()})
    return render(request, 'vine/vine_index.html', {'all_vines': Vine.objects.all()})

def CreateVineAlbum(request):
    form = VineAlbum_form(request.POST or None, request.FILES or None)
    userprofile = request.user.profile
    if(request.method == "POST"):
        if form.is_valid():
            album=form.save(commit=False)
            album.profile = userprofile
            album.vine_logo = request.FILES['vine_logo']
            album.save()
           # userprofile.add_album(album)
            all_albums = VineAlbum.objects.filter(profile=userprofile)
            return render(request, 'vine/myAlbums.html', {'all_albums':  all_albums})
    return render(request, 'vine/vinealbum_form.html',{'form':form})

class UpdateVineAlbum(generic.UpdateView):
    model = VineAlbum
    fields = ['artist', 'title', 'genre', 'vine_logo']
    #template_name_suffix = '_update_form'
    success_url = reverse_lazy('Vine:my-album')

def DeleteVineAlbum(request,album_id):
    if not request.user.is_authenticated:
        return render(request, 'vine/login.html')
    album = get_object_or_404(VineAlbum, pk=album_id)
    userprofile = request.user.profile
    #userprofile.delete_album(album)
    album.delete()
    all_albums = VineAlbum.objects.filter(profile=userprofile)
    return render(request, 'vine/myAlbums.html', {'all_albums': all_albums})


def CreateVine(request,album_id):
    form = Vine_form(request.POST or None, request.FILES or None)
    userprofile = request.user.profile
    album = get_object_or_404(VineAlbum, pk=album_id)
    if (request.method == "POST"):
        if form.is_valid():
            vine = form.save(commit=False)
            vine.album = album
            vine.video = request.FILES['video']
            vine.save()
            #userprofile.add_vine(album.title,vine)
            return render(request, 'vine/myVines.html', {'album': album})
    return render(request, 'vine/vine_form.html', {'form': form})


class UpdateVine(generic.UpdateView):
    model = Vine
    fields = ['vine_title','album','language','country','video']
    success_url = reverse_lazy('Vine:my-album')

def DeleteVine(request,album_id,vine_id):
    if not request.user.is_authenticated:
        return render(request, 'vine/login.html')
    album = get_object_or_404(VineAlbum, pk=album_id)
    vine =  album.vine_set.get(pk=vine_id)
    userprofile = request.user.profile
    vine.delete()
    return render(request, 'vine/myVines.html', {'album': album})


def myAlbum(request):
    if not request.user.is_authenticated:
        return render(request, 'vine/login.html')
    userprofile = request.user.profile
    all_albums= VineAlbum.objects.filter(profile = userprofile)
    return render(request, 'vine/myAlbums.html', {'all_albums':  all_albums})

def myVines(request,album_id):
    if not request.user.is_authenticated:
        return render(request, 'vine/login.html')
    userprofile = request.user.profile
    album = get_object_or_404(VineAlbum, pk=album_id)
    return render(request, 'vine/myVines.html', {'album':  album})

def register(request):
    form = UserForm(request.POST or None)
    if(request.method == 'POST'):
        if(form.is_valid()):
            user = form.save(commit=False)
            username = form.cleaned_data.get('username')
            email = form.cleaned_data.get('email')
            password = form.cleaned_data.get('password')
            user.set_password(password)
            user.save()
            user = authenticate(username=username, password=password)
            if user is not None:
                profile = Profile()
                profile.user = user
                profile.about_me = form.cleaned_data.get('about_me')
                profile.save()
                if user.is_active:
                    login(request, user)
                    #return render(request, 'vine/index.html', {'all_albums': VineAlbum.objects.all()})
                    return HttpResponseRedirect(reverse('Vine:index'))
    return render(request, 'vine/register.html', {'form': form})

def logout_user(request):
    logout(request)
    return render(request, 'vine/base_visitor.html',  {'all_albums': VineAlbum.objects.all()})

def login_user(request):
    form = Login(request.POST or None)
    if request.method == "POST":
        user = request.POST['username']
        password = request.POST['password']
        user_to = authenticate(username=user, password=password)
        if user_to is not None:
            if user_to.is_active:
                login(request, user_to)
                #return render(request, 'vine/index.html', {'all_albums': VineAlbum.objects.all()})
                return redirect(reverse('Vine:index'))
        else:
            return render(request, 'vine/login.html', {'error_message': 'Invalid login'})
    return render(request, 'vine/login.html', {'form': form})

def profile(request):
    user = request.user.profile
    render(request,'vine/profile.html')