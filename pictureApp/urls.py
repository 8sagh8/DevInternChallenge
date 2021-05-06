from django.urls import path, include
from . import views

app_name = "pictureApp"

urlpatterns = [
    path('', views.index, name="index"),
    path('index', views.index, name="index"),
    # path('modifyPhoto/<_id>', views.modifyPhoto, name="modifyPhoto"),
    path('persistPhoto/<_id>', views.persistPhoto, name="persistPhoto"),
    path('deletePhoto/<_id>', views.deletePhoto, name="deletePhoto"),
    path('deleteMultiPhoto/', views.deleteMultiPhoto, name="deleteMultiPhoto"),
    path('searchPhoto/', views.searchPhoto, name="searchPhoto"),
    path('statusChange/<_id>', views.statusChange, name="statusChange"),
]
