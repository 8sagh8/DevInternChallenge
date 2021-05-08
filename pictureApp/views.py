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
        temp = []   # at Index 0 will store True/False and Index 1 will store photo object
        if currentUser == p.user:
            temp.append(True)   # TRUE is to show edit button
            temp.append(p)
            photoList.append(temp)
        elif p.status == False:
            temp.append(False)  # FALSE is to hide edit buttons
            temp.append(p)
            photoList.append(temp)
    photoList.reverse()

    return photoList

# Create your views here.
def index(request):
    is_sign_in = isSignIn(request)  #get is signed in

    if request.method == "POST":
        form=PhotoForm(data=request.POST,files=request.FILES)
        if form.is_valid():
            form.save()
            temp = Photo.objects.latest('id')
            temp.user = str(request.user)
            temp.save()
    else:
        form=PhotoForm() 
    
    photoList = currentPhoto(request)

    return render(request,"pictureApp/index.html", {
        "photo":photoList, 
        "form": form,
        "isSignIn": is_sign_in
        })

# Add Multiple Photos
def addMultiplePhotos(request):
    if request.method == "POST":
        images = request.FILES.getlist('images')
        for i in images:
            photo = Photo.objects.create(title="New", image=i, user=str(request.user))
            photo.save()

    return redirect('/')

def deletePhoto(request, _id):
    photo_obj = Photo.objects.get(id=eval(_id)) # get photo object by id
    file_path = 'static/photosFolder/' + str(photo_obj.image)   # get file full path
    os.remove(file_path)    # delete file from local folder
    photo_obj.delete()      # delete object data from database

    return redirect("/") 

def deleteMultiPhoto(request):
   
    print("~~~~~ I am In deleteMulti", flush=True )
    if request.method == 'POST':
        id_List = request.POST.getlist('data[]')

        for _id in id_List:
            p_obj = Photo.objects.get(id=eval(_id))
            file_path = 'static/photosFolder/' + str(p_obj.image)   # get file full path
            os.remove(file_path)    # delete file from local folder
            p_obj.delete()

    return ("done");
    print("******* I am done", flush=True)
    # return json(success, "done", 200)
    # return redirect('/')

# Persisting Photo title after modification
def persistPhoto(request, _id):
    if request.method == "POST":
        title = request.POST['newTitle']
        photo_obj = Photo.objects.get(id=eval(_id))
        photo_obj.title= title
        photo_obj.save()

    return redirect ("/")

# Search Photo by title provided by user
def searchPhoto(request):
    is_sign_in = isSignIn(request)  #get is signed in
    search_value = None
    form=PhotoForm()
    photoList = []
    obj = Photo.objects.all()

    if request.method == 'POST':
        search_value = request.POST['search_input']
        search_value = search_value.lower()

    if search_value != None:
        for p in obj:
            temp = []
            if search_value in p.title.lower():
                if str(request.user) == p.user:
                    temp.append(True)   # Allow rights to edit photos
                    temp.append(p)
                    photoList.append(temp)
                else:
                    temp.append(False)   # Dont allow to edit photos
                    if p.status == False:    # False means others' user photo is public
                        temp.append(p)
                        photoList.append(temp)
            
        photoList.reverse()

    return render(request,"pictureApp/index.html", {
        "isSignIn": is_sign_in,
        "form": form,
        "photo": photoList
    })
        

# change status from Private to Public and ViceVersa
def statusChange(request, _id):
    photo_obj = Photo.objects.get(id = eval(_id))
    if photo_obj.status == True:
        photo_obj.status = False
    else:
        photo_obj.status = True
    photo_obj.save()

    return redirect('/')

# to display only Current User's Private Photos
def userPrivatePhotos(request):
    is_sign_in = isSignIn(request)  #get is signed in
    form=PhotoForm()    
    photoList = []
    obj = Photo.objects.all()

    for p in obj:
        if str(request.user) == p.user:
            temp = []
            if p.status == True:    # True means photos status is Private
                temp.append(True)   # True allow permission to edit
                temp.append(p)
                photoList.append(temp)

    return render(request,"pictureApp/index.html", {
        "photo": photoList, 
        "form": form,
        "isSignIn": is_sign_in
        })

# to display only Current User's Public Photos
def userPublicPhotos(request):
    is_sign_in = isSignIn(request)  #get is signed in
    form=PhotoForm()    
    photoList = []
    obj = Photo.objects.all()

    for p in obj:
        if str(request.user) == p.user:
            temp = []
            if p.status == False:    # False means photos status is Public
                temp.append(True)   # True allow permission to edit
                temp.append(p)
                photoList.append(temp)

    return render(request,"pictureApp/index.html", {
        "photo": photoList, 
        "form": form,
        "isSignIn": is_sign_in
        })

# to display only Current User's All Photos
def userAllPhotos(request):
    is_sign_in = isSignIn(request)  #get is signed in
    form=PhotoForm()    
    photoList = []
    obj = Photo.objects.all()

    for p in obj:
        temp = []
        if str(request.user) == p.user:
            temp.append(True)   # True allow permission to edit
            temp.append(p)
            photoList.append(temp)

    return render(request,"pictureApp/index.html", {
        "photo": photoList, 
        "form": form,
        "isSignIn": is_sign_in
        })

# to display All Public Photo of Current User's and Other Users
def allPublicPhotos(request):
    is_sign_in = isSignIn(request)  #get is signed in
    form=PhotoForm()    
    photoList = []
    obj = Photo.objects.all()

    for p in obj:
        temp = []
        if p.status == False:   # False means status is Public
            if str(request.user) == p.user:
                temp.append(True)   # True allow permission to edit
                temp.append(p)
                photoList.append(temp)
            else:
                temp.append(False)   # False don't grant permission to edit
                temp.append(p)
                photoList.append(temp)

    return render(request,"pictureApp/index.html", {
        "photo": photoList, 
        "form": form,
        "isSignIn": is_sign_in
        })
### Log out View
def logout(request):
    auth.logout(request) # logout
    return redirect('/')


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
    form=PhotoForm()
    photoList = currentPhoto(request)

    return render(request, 'pictureApp/index.html', {
        "photo": photoList,
        "form": form,
        "isSignIn": is_sign_in,
        "isValidEntry": isValidEntry,
    })
