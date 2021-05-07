from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.http import HttpResponse
from .models import *
import os 

from .form import *



#Function to know SignIn or Not
def isSignIn(request):
    returning_value = True
    if "AnonymousUser" == str(request.user):
        returning_value = False
    return returning_value

#Function to get Current User's Photo and others Public Only
def currentPhoto(request):
    photoList = []
    currentUser = str(request.user)     #name of current user
    photo=Photo.objects.all()

    for p in photo:
        temp = []
        if currentUser == p.user:
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
    is_sign_in = isSignIn(request)  #get is signed in

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
        "isSignIn": is_sign_in
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
    is_sign_in = isSignIn(request)  #get is signed in

    if request.method == "POST":
        title = request.POST['newTitle']
        photo_obj = Photo.objects.get(id=eval(_id))
        photo_obj.title= title
        photo_obj.save()

    photoList = currentPhoto(request)

    return redirect ("/", {
        "photo": photoList,
        "form": form,
        "isSignIn": is_sign_in
    })



def deletePhoto(request, _id):
    photo_obj = Photo.objects.get(id=eval(_id)) # get photo object by id
    file_path = 'static/photosFolder/' + str(photo_obj.image)   # get file full path
    os.remove(file_path)    # delete file from local folder
    photo_obj.delete()      # delete object data from database
    is_sign_in = isSignIn(request)  #get is signed in

    form=ImageForm()
    photoList = currentPhoto(request)
    
    return redirect("/", {
        "photo": photoList,
        "form": form,
        "isSignIn": is_sign_in
    }) 

def deleteMultiPhoto(request):
    is_sign_in = isSignIn(request)  #get is signed in

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
        "form": form,
        "isSignIn": is_sign_in
    })

def searchPhoto(request):
    is_sign_in = isSignIn(request)  #get is signed in
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

    return redirect('/', {
        "photo": photoList,
        "form": form,
        "isSignIn": is_sign_in
    })

def statusChange(request, _id):
    is_sign_in = isSignIn(request)  #get is signed in
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
        "form": form,
        "isSignIn": is_sign_in
    })

### Log out View
def logout(request):
    auth.logout(request)            # logout
    is_sign_in = isSignIn(request)  # get is signed in
    form=ImageForm()
    photoList = currentPhoto(request)

    return redirect('/', {
        "photo": photoList,
        "form": form,
        "isSignIn": is_sign_in
    })

### Login View
def login(request):
    isValidEntry= False
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        
        user = auth.authenticate(username = username, password = password)

        if user is not None:
            auth.login(request, user)
            
        else:
            isValidEntry = True
            
    is_sign_in = isSignIn(request)  # get is signed in
    form=ImageForm()
    photoList = currentPhoto(request)

    return render(request, 'pictureApp/index.html', {
        "photo": photoList,
        "form": form,
        "isSignIn": is_sign_in,
        "isValidEntry": isValidEntry,
    })
