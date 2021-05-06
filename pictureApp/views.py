from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import os 

from .form import *

# Create your views here.
def index(request):
    photoList = []
    if request.method == "POST":
        form=ImageForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
    else:
        form=ImageForm() 

    photo=Photo.objects.all()
    for p in photo:
        photoList.append(p)

    photoList.reverse()
    return render(request,"pictureApp/index.html", {
        "photo":photoList, 
        "form": form,
        })

# Create your views here.
def modifyPhoto(request, _id):
    obj = Photo.objects.all()
    form=ImageForm()  
    photoList = []
    for p in obj:
        if str(p.id) == _id:
            photoList.append(p)
    
    return render(request,"pictureApp/modify.html", {
        "photo":photoList, 
        "form": form
        })

# Persisting Photo title after modification
def persistPhoto(request, _id):
    form=ImageForm()
    photoList = []

    if request.method == "POST":
        title = request.POST['newTitle']
        photo_obj = Photo.objects.get(id=eval(_id))
        photo_obj.title= title
        photo_obj.save()

    obj = Photo.objects.all()
    for p in obj:
        photoList.append(p) 
    photoList.reverse()

    return redirect ("/", {
        "photo": photoList,
        "form": form
    })



def deletePhoto(request, _id):
    photo_obj = Photo.objects.get(id=eval(_id))
    print("image name:", photo_obj.image, flush=True)
    photo_obj.delete()

    form=ImageForm()
    photoList = []

    obj = Photo.objects.all()
    for p in obj:
        photoList.append(p) 
    photoList.reverse()
    
    return redirect("/", {
        "photo": photoList,
        "form": form
    }) 

def deleteMultiPhoto(request):
 
    if request.method == 'POST':
        id_List = request.POST.getlist('data[]')

        for _id in id_List:
            p_obj = Photo.objects.get(id=eval(_id))
            p_obj.delete()

    form=ImageForm()
    photoList = []

    obj = Photo.objects.all()
    for p in obj:
        photoList.append(p) 
    photoList.reverse()

    return redirect('/', {
        "photo": photoList,
        "form": form
    })

def searchPhoto(request):
    search_value = None
    form=ImageForm()
    photoList = []
    obj = Photo.objects.all()

    if request.method == 'POST':
        search_value = request.POST['search_input']

    if search_value != None:
        for p in obj:
            if search_value in p.title:
                photoList.append(p)
    
    photoList.reverse()

    return render(request, 'pictureApp/index.html', {
        "photo": photoList,
        "form": form,
    })


