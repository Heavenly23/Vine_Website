from django.contrib import admin
from django.urls import path
from . import views

app_name = 'vine'

urlpatterns = [
              # vine/
              path('', views.IndexView, name='index'),

              path('vines/', views.vine_Index, name='vine_index'),
              # vine/1
              path('<int:album_id>/', views.DetailView, name='detail'),

              # vine/1/2
              path('<int:album_id>/<int:vine_id>/', views.DetailView_vine, name='vine_detail'),

              # vine/album/add
              path('album/add/', views.CreateVineAlbum, name='album-add'),

              path('album/<int:pk>/update/', views.UpdateVineAlbum.as_view(), name='album-update'),

              path('album/<int:album_id>/delete/', views.DeleteVineAlbum, name='album-delete'),

               # vine/add/1
              path('album/add/vine/<int:album_id>',views.CreateVine, name='vine-add'),

              path('my_album/',views.myAlbum, name='my-album'),

              path('my_album/<int:album_id>/vines/',views.myVines, name='my-vine'),

              path('my_album/<int:album_id>/update/<int:pk>/',views.UpdateVine.as_view(), name='vine-update'),

              path('my_album/<int:album_id>/delete/<int:vine_id>/',views.DeleteVine, name='vine-delete'),

              path('register',views.register,name="create-account"),

              path('log-in',views.login_user,name="login"),

              path('log-out',views.logout_user,name="logout"),

]