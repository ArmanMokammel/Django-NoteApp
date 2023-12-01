from django.conf import settings
from django.shortcuts import redirect, render
from django.contrib import messages
from django.contrib.auth.models import User,auth
from UserData.models import ImageFile, UserInfo, UserNotes
# from .models import UserInfo
from django.contrib.auth.decorators import login_required

# Create your views here.
def landingPage(request):
    if(request.method == "POST"):
        if('login' in request.POST):
            username = request.POST['login_username']
            password = request.POST['login_password']

            user = auth.authenticate(username=username, password=password)
            if(user is not None):
                auth.login(request, user)
                return redirect('UserData:notes_home', username)
            else:
                messages.error(request, "Credentials don't match")
        elif('signup' in request.POST):
            email = request.POST['signup_email']
            username = request.POST['signup_username']
            password = request.POST['signup_password']
            confirm_password = request.POST['signup_cpassword']
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
                    return redirect('UserData:landing_page')
            else:
                messages.error(request,"Two Passwords do not match")

    return render(request, 'index.html')

# def signup(request):
#     if(request.method == "POST"):
#         email = request.POST['email']
#         username = request.POST['username']
#         password = request.POST['password']
#         confirm_password = request.POST['confirm_password']
#         if(confirm_password == password):
#             if(User.objects.filter(username=username).exists()):
#                 messages.error(request, "User already exists")
#             else:
#                 new_user = User.objects.create_user(username=username, email=email, password=password)
#                 new_user.save()

#                 new_user_for_table = UserInfo.objects.create(email=email, username=username)
#                 new_user_for_table.save()
#                 print("User stored in database")

#                 messages.success(request, "Account Created Successfully")
#                 return redirect('UserData:login')
#         else:
#             messages.error(request,"Two Passwords do not match")
#     return render(request, 'signup.html')

# def login(request):
#     if(request.method == "POST"):
#         username = request.POST['username']
#         password = request.POST['password']

#         user = auth.authenticate(username=username, password=password)
#         if(user is not None):
#             auth.login(request, user)
#             return redirect('UserData:notes_home', username)
#         else:
#             messages.error(request, "Credentials don't match")

#     return render(request, 'login.html')

@login_required
def notes_home(request, username):
    if(request.user.username != username):
        return redirect('UserData:notes_home', request.user.username)
    
    get_all_notes = UserNotes.objects.filter(username=username)
    context={
        'usernameee' : username,
        'all_notes' : get_all_notes
    }
    return render(request, 'notes_home.html', context=context)

@login_required
def add_note(request, username):
    if(request.user.username != username):
        return redirect('UserData:add_note', request.user.username)
    
    if(request.method == "POST"):
        title = request.POST['title']
        description = request.POST['note_description']
        tags = None
        image = None
        if('tags_array' in request.POST):
            tagsString = request.POST['tags_array']
            remove_char = ['[', ']', '"']
            for char in remove_char:
                tagsString = tagsString.replace(char,'') 
            tags = tagsString
                
        new_note = UserNotes.objects.create(title=title, description=description, tags=tags, username=UserInfo.objects.get(username=username))
        
        if('images' in request.FILES):
            for file in request.FILES.getlist('images'):
                image = ImageFile.objects.create(image=file, user_note=new_note)
                image.save()

        new_note.save()
        return redirect('UserData:notes_home', username)
    
    context={
        'usernameee' : username
    }

    return render(request, 'add_note.html', context=context)

@login_required
def note_description(request, username, id):
    if(request.user.username != username or not UserNotes.objects.filter(username=request.user.username, pk=id).exists()):
        return redirect('UserData:notes_home', request.user.username)
    
    # if(request.method == "POST"):
    #     elif ('delete_note' in request.POST):
    #         user_note = UserNotes.objects.get(pk=id)
    #         user_note.image.delete()
    #         user_note.delete()
    #         return redirect('UserData:notes_home', username)

    user_note = UserNotes.objects.get(pk=id)
    user_images = ImageFile.objects.filter(user_note=user_note)
    context = {
        'usernameee' : username,
        'user_images':user_images,
        'user_note' : user_note,
        'mediaUrl' : settings.MEDIA_URL
    }
    return render(request, 'view_note.html', context=context)

@login_required
def update_note(request, username, id):
    if(request.user.username != username or not UserNotes.objects.filter(username=request.user.username, pk=id).exists()):
        return redirect('UserData:notes_home', request.user.username)
    
    user_note = UserNotes.objects.get(pk=id)
    user_images = ImageFile.objects.filter(user_note=user_note)
    
    if(request.method == "POST"):
        title = request.POST['title']
        description = request.POST['note_description']
        user_note = UserNotes.objects.get(pk=id)
        user_note.title = title
        user_note.description = description

        if('tags_array' in request.POST):
                tagsString = request.POST['tags_array']
                remove_char = ['[', ']', '"']
                for char in remove_char:
                    tagsString = tagsString.replace(char,'') 
                user_note.tags = tagsString
        else:
            user_note.tags = None

        if('images' in request.FILES):
            for image in request.FILES.getlist('images'):
                image = ImageFile.objects.create(image=image, user_note=user_note)
                image.save()

        user_note.save()
        return redirect('UserData:notes_home', username)
    
    context = {
        'usernameee' : username,
        'user_note' : user_note,
        'images' : user_images,
        'mediaUrl' : settings.MEDIA_URL
    }
    return render(request, 'note_description.html', context=context)

def delete_note(request, username, id):
    user_note = UserNotes.objects.get(pk=id)
    user_images = ImageFile.objects.filter(user_note=user_note)

    for image in user_images:
        image.image.delete()
        image.delete()
    user_note.delete()

    return redirect('UserData:notes_home', username)

def logout(request):
    auth.logout(request)
    return redirect('UserData:landing_page')

