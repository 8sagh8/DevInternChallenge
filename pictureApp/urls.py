from django.urls import path, include
from . import views

app_name = "pictureApp"

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name="index"),
    path('addMultiplePhotos', views.addMultiplePhotos, name="addMultiplePhotos"),
    path('persistPhoto/<_id>', views.persistPhoto, name="persistPhoto"),
    path('deletePhoto/<_id>', views.deletePhoto, name="deletePhoto"),
    path('deleteMultiPhoto/', views.deleteMultiPhoto, name="deleteMultiPhoto"),
    path('searchPhoto/', views.searchPhoto, name="searchPhoto"),
    path('statusChange/<_id>', views.statusChange, name="statusChange"),
    path('userPrivatePhotos', views.userPrivatePhotos, name="userPrivatePhotos"),
    path('userPublicPhotos', views.userPublicPhotos, name="userPublicPhotos"),
    path('userAllPhotos', views.userAllPhotos, name="userAllPhotos"),
    path('allPublicPhotos', views.allPublicPhotos, name="allPublicPhotos"),
    path('logout', views.logout, name="logout"),
    path('login', views.login, name="login"),
]
