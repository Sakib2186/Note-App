from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import UserInfo,UserNotes, NoteImage,Notes_Label
from django.conf import settings
from django.utils import timezone
import os
import datetime
from . forms import NoteForm

from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def landingPage(request):
    return render(request,'index.html')

def login(request):
    if request.method=="POST":
        username=request.POST['username']
        password=request.POST['password']
    
        user=auth.authenticate(username=username,password=password)
        if user is not None:
            auth.login(request,user)
            return redirect('UserData:notes_home',username)
        else:
            print("Credentials dont match")
            
    return render(request,'login.html')

def signup(request):
    if request.method=="POST":
        email=request.POST['email']
        username=request.POST['username']
        password=request.POST['password']
        confirm_password=request.POST['confirm_password']
        if(password==confirm_password):
            if(User.objects.filter(username=username).exists()):
                messages.error(request,"User already exists")            
            else:
                new_user=User.objects.create_user(username=username,email=email,password=password)
                new_user.save()
                
                new_user_for_table=UserInfo.objects.create(email=email,username=username)
                new_user_for_table.save()
                print("User stored in database")
                messages.success(request,"Account Created Successfully")
                return redirect('UserData:login')
        else:
            messages.error(request,"Two Passwords do not match")
    return render(request,'signup.html')

def logout(request):
    auth.logout(request)
    return redirect('UserData:login')

@login_required
def notes_home(request,username):
    username=request.user.username
    get_all_notes=UserNotes.objects.filter(username=username).order_by('-created_at')
    print(get_all_notes)
    context={
        'username2':username,
        'all_notes':get_all_notes,
    }
    return render(request,'notes_home.html',context=context)

@login_required
def add_note(request, username):
    user = request.user.username
    labels = Notes_Label.objects.filter(label_for = UserInfo.objects.get(username=user))
    form = NoteForm()

    if request.method == "POST":
        if request.POST.get('create_note'):
            title = request.POST['title']
            created_at=timezone.now()
            note_description = request.POST['description']
            label = request.POST.getlist('label')
            print(label)
            files = request.FILES.getlist('image')  # Get a list of uploaded files
            if len(label)==0:
                new_note = UserNotes.objects.create(
                    title=title,
                    created_at=created_at,
                    description=note_description,
                    username=UserInfo.objects.get(username=user)
                )
                new_note.save()
            else:
                new_note = UserNotes.objects.create(
                    title=title,
                    description=note_description,
                    username=UserInfo.objects.get(username=user)
                )
                string =""
                for i in label:
                    print(i)
                    string = string + str(i) + ","
                print("String is "+ string)
                new_note.note_label = string
                new_note.save()


            for file in files:
                NoteImage.objects.create(note=new_note, image=file)

            return redirect('UserData:notes_home', username)
    
        if request.POST.get('add_labels'):
            username=request.user.username
            label_name = request.POST['label']
            new_label = Notes_Label.objects.create(labelName=label_name,label_for =UserInfo.objects.get(username=username))
            new_label.save()

    
    context={'label':labels,
             'form':form,
             'username2':username}

    return render(request, 'add_note.html',context)

@login_required
def note_description(request, pk):
    username=request.user.username
    note = UserNotes.objects.get(username=username,pk=pk)
    image_count = note.images.count()
    column_size = 12 // image_count if image_count > 0 else 12 
     
    if request.method == 'POST':
        note.delete()
        return redirect('UserData:notes_home', username)


    context = {
        'username2':username,
        'pk':pk,
        'note': note,
    }

    return render(request, 'note_description.html', context)


@login_required
def notes_edit(request,pk):
    instance = get_object_or_404(UserNotes, pk=pk)
    form = NoteForm(request.POST or None, instance=instance)
    username = request.user.username
    labels = Notes_Label.objects.filter(label_for = UserInfo.objects.get(username=username))
    image = NoteImage.objects.filter(note = UserNotes.objects.get(pk=pk))
    note = UserNotes.objects.get(username=username,pk=pk)
    title = note.title
    description = note.description
    note_label = note.note_label
    print(note_label)
    try:
        note_label = note_label.split(",")
    except:
        note_label=[]
    
    label = []
    for i in labels:
        label.append(i.labelName)
   

    if request.method == "POST":
        if request.POST.get('add_labels'):
            username=request.user.username
            label_name = request.POST['label']
            new_label = Notes_Label.objects.create(labelName=label_name,label_for =UserInfo.objects.get(username=username))
            new_label.save()

        if request.POST.get('edit_note'):
            title = request.POST['title']
            note_description = request.POST['description']
            label = request.POST.getlist('label')
            files = request.FILES.getlist('image')
            print(label)

            if len(files)>0:
                for i in image:
                    path = settings.MEDIA_ROOT+str(i.image)
                    os.remove(path)
                    i = image.delete()
                    
                for file in files:
                    NoteImage.objects.create(note=note, image=file)


            note.title = title
            note.created_at=datetime.datetime.now()
            note.description = note_description
            string =""
            for i in label:
                print(i)
                string = string + str(i) + ","
            note.note_label = string
            note.date = datetime.datetime.now()
            note.save()
            return redirect('UserData:note_description',pk)


    context = {
            'username2':username,
            'pk':pk,
            'title':title,
            'description':description,
            'label':note_label,
            'all_label':label,
            'images':image,
            'media_url':settings.MEDIA_URL,
            'form':form}


    return render(request,"notes_edit.html",context)



