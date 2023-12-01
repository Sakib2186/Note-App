from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import UserInfo,UserNotes, NoteImage,Notes_Label
from django.conf import settings


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
    get_all_notes=UserNotes.objects.filter(username=username)
    print(get_all_notes)
    context={
        'username2':username,
        'all_notes':get_all_notes,
    }
    return render(request,'notes_home.html',context=context)

@login_required
def add_note(request, username):
    labels = Notes_Label.objects.all()


    if request.method == "POST":
        if request.POST.get('create_note'):
            title = request.POST['title']
            note_description = request.POST['note_description']
            label = request.POST.getlist('label')
            print(label)
            files = request.FILES.getlist('image')  # Get a list of uploaded files
            user = request.user.username
            if len(label)==0:
                new_note = UserNotes.objects.create(
                    title=title,
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
                    string = string + str(i) + " "
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
             }

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
    username=request.user.username
    labels = Notes_Label.objects.all()
    image = NoteImage.objects.filter(note = UserNotes.objects.get(pk=pk))
    note = UserNotes.objects.get(username=username,pk=pk)
    title = note.title
    description = note.description
    note_label = note.note_label
    note_label = note_label.split()
    print(note_label)
    label = []
    for i in labels:
        label.append(i.labelName)
    print(label)

    if request.method == "POST":
        if request.POST.get('add_labels'):
            username=request.user.username
            label_name = request.POST['label']
            new_label = Notes_Label.objects.create(labelName=label_name,label_for =UserInfo.objects.get(username=username))
            new_label.save()
        





    context = {'title':title,
               'description':description,
               'label':note_label,
               'all_label':label,
               'images':image,
               'media_url':settings.MEDIA_URL,}


    return render(request,"notes_edit.html",context)



