from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User,auth
from UserData.models import UserInfo, UserNotes
# from .models import UserInfo
from django.contrib.auth.decorators import login_required

# Create your views here.
def landingPage(request):
    return render(request, 'index.html')

def signup(request):
    if(request.method == "POST"):
        email = request.POST['email']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        if(confirm_password == password):
            if(User.objects.filter(username=username).exists()):
                messages.error(request, "User already exists")
            else:
                new_user = User.objects.create_user(username=username, email=email, password=password)
                new_user.save()

                new_user_for_table = UserInfo.objects.create(email=email, username=username)
                new_user_for_table.save()
                print("User stored in database")

                messages.success(request, "Account Created Successfully")
                return redirect('UserData:login')
        else:
            messages.error(request,"Two Passwords do not match")
    return render(request, 'signup.html')

def login(request):
    if(request.method == "POST"):
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)
        if(user is not None):
            auth.login(request, user)
            return redirect('UserData:notes_home', username)
        else:
            messages.error(request, "Credentials don't match")

    return render(request, 'login.html')

@login_required
def notes_home(request, username):
    get_all_notes = UserNotes.objects.filter(username=username)
    context={
        'usernameee' : username,
        'all_notes' : get_all_notes
    }
    return render(request, 'notes_home.html', context=context)

@login_required
def add_note(request, username):
    if(request.method == "POST"):
        title = request.POST['title']
        description = request.POST['note_description']
        image = None
        if('image' in request.FILES):
            image = request.FILES['image']

        new_note = UserNotes.objects.create(title=title, description=description, image=image, username=UserInfo.objects.get(username=username))
        new_note.save()
        print("Notes taken")
        return redirect('UserData:notes_home', username)

    return render(request, 'add_note.html')

@login_required
def note_description(request, username, id):
    if(request.method == "POST"):
        if('update_note' in request.POST):
            title = request.POST['title']
            description = request.POST['note_description']
            
            user_note = UserNotes.objects.get(pk=id)

            user_note.title = title
            user_note.description = description
            if('image' in request.FILES):
                image = request.FILES['image']
                user_note.image = image

            user_note.save()
            return redirect('UserData:notes_home', username)
        elif ('delete_note' in request.POST):
            user_note = UserNotes.objects.get(pk=id)
            user_note.image.delete()
            user_note.delete()
            return redirect('UserData:notes_home', username)

    user_note = UserNotes.objects.get(pk=id)
    context = {
        'user_note' : user_note,
        'mediaUrl' : settings.MEDIA_URL
    }
    return render(request, 'note_description.html', context=context)

def logout(request):
    auth.logout(request)
    return redirect('UserData:login')


