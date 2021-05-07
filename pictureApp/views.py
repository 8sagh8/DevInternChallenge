from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import *
import os 

from .form import *

#Function to get Current User's Photo and others Public Only
def currentPhoto(request):
    photoList = []
    currentUser = (request.user)
    photo=Photo.objects.all()
    
    for p in photo:
        temp = []
        if str(currentUser) == p.user:
            temp.append(True)
            temp.append(p)
            photoList.append(temp)
        elif p.status == False:
            temp.append(False)
            temp.append(p)
            photoList.append(temp)
    photoList.reverse()

    return photoList

# Create your views here.
def index(request):
    auth_person = request.user
    
    if request.method == "POST":
        form=ImageForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            temp = Photo.objects.latest('id')
            temp.user = str(request.user)
            temp.save()
    else:
        form=ImageForm() 
    
    photoList = currentPhoto(request)

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

    if request.method == "POST":
        title = request.POST['newTitle']
        photo_obj = Photo.objects.get(id=eval(_id))
        photo_obj.title= title
        photo_obj.save()

    photoList = currentPhoto(request)

    return redirect ("/", {
        "photo": photoList,
        "form": form
    })



def deletePhoto(request, _id):
    photo_obj = Photo.objects.get(id=eval(_id)) # get photo object by id
    file_path = 'static/photosFolder/' + str(photo_obj.image)   # get file full path
    os.remove(file_path)    # delete file from local folder
    photo_obj.delete()      # delete object data from database

    form=ImageForm()
    photoList = currentPhoto(request)
    
    return redirect("/", {
        "photo": photoList,
        "form": form
    }) 

def deleteMultiPhoto(request):
    print("~~~~~ I am In deleteMulti", flush=True )
    if request.method == 'POST':
        id_List = request.POST.getlist('data[]')

        for _id in id_List:
            p_obj = Photo.objects.get(id=eval(_id))
            file_path = 'static/photosFolder/' + str(photo_obj.image)   # get file full path
            os.remove(file_path)    # delete file from local folder
            p_obj.delete()

    form=ImageForm()
    photoList = currentPhoto(request)

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
            if p.status == False or (p.user == str(request.user)): 
                if search_value in p.title.lower():
                    photoList.append(p)
    
    photoList.reverse()

    return render(request, 'pictureApp/index.html', {
        "photo": photoList,
        "form": form,
    })

def statusChange(request, _id):
    photo_obj = Photo.objects.get(id = eval(_id))
    if photo_obj.status == True:
        photo_obj.status = False
    else:
        photo_obj.status = True
    photo_obj.save()

    form=ImageForm()
    photoList = currentPhoto(request)

    return redirect('/', {
        "photo": photoList,
        "form": form
    })


