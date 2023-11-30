from django.shortcuts import render,redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.models import User,auth
from .models import UserInfo,UserNotes, NoteImage
from django.contrib.auth.decorators import login_required
# Create your views here.

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
    get_all_notes=UserNotes.objects.filter(username=username)
    print(get_all_notes)
    context={
        'username2':username,
        'all_notes':get_all_notes,
    }
    return render(request,'notes_home.html',context=context)

@login_required
def add_note(request, username):
    if request.method == "POST":
        title = request.POST['title']
        note_description = request.POST['note_description']
        files = request.FILES.getlist('image')  # Get a list of uploaded files
        user = request.user.username

        new_note = UserNotes.objects.create(
            title=title,
            description=note_description,
            username=UserInfo.objects.get(username=user)
        )

        for file in files:
            NoteImage.objects.create(note=new_note, image=file)

        return redirect('UserData:notes_home', username)

    return render(request, 'add_note.html')

@login_required
def note_description(request, pk):
    note = get_object_or_404(UserNotes, pk=pk)
    username=request.user.username
     
    if request.method == 'POST':
        note.delete()
        return redirect('UserData:notes_home', username)


    context = {
        'username2':username,
        'note': note,
    }

    return render(request, 'note_description.html', context)