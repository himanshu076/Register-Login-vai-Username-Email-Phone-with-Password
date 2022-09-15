from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from account.models import CustomUser, Profile
from itertools import chain
import random

# Create your views here.


def home(request):
    return render(request, 'account/index.html', {})

def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['confirm_password']

        if password == password2:
            if CustomUser.objects.filter(email=email).exists():
                messages.info(request, 'Email Taken')
                return redirect('login')
            else:
                user = CustomUser.objects.create_user(email=email, password=password)
                user.save()
                return redirect('login')

                # log user in and redirect to settings page
                # user_login = authenticate(username=user, password=password)
                # login(request, user_login)

                # # create the profile for the new user
                # user_model = User.objects.get(username=username)
                # new_profile = Profile.objects.create(user=user_model, id_user=user_model.id)
                # new_profile.save()
                # return redirect('settings')
        else:
            messages.info(request, 'Password Not Matching')
            return redirect('register')

    else:
        return render(request, 'account/register.html')


def login(request):
    if request.user.is_authenticated:
        return redirect("home")
    else:
        if request.method == "POST":
            username = request.POST["email"]
            password = request.POST["password"]
            if username and password:
                user = authenticate(username=username, password=password)
                if user:
                    auth_login(request, user)
                    return redirect("home")
    return render(request, "account/login.html", {})

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def profile(request):

    if request.method == "POST":
        user = request.user.email
        image = request.FILES.get('image_upload')
        # caption = request.POST['caption']

        new_post = Profile.objects.create(user=user, image=image)
        new_post.save()

        return redirect('/')

    return redirect(request, 'account/profile.html', {})


# @login_required(login_url='signin')
# def profile(request, pk):
#     user_object = User.objects.get(username=pk)
#     user_profile = Profile.objects.get(user=user_object)
#     user_posts = Post.objects.filter(user=pk)
#     user_post_length = len(user_posts)

#     follower = request.user.username
#     user = pk

#     if FollowersCount.objects.filter(follower=follower, user=user).first():
#         button_text = 'Unfollow'
#     else:
#         button_text = 'Follow'

#     user_followers = len(FollowersCount.objects.filter(user=pk))
#     user_following = len(FollowersCount.objects.filter(follower=pk))

#     context = {'user_object': user_object,
#                 'user_profile': user_profile,
#                 'user_post': user_posts,
#                 'user_post_length': user_post_length,
#                 'button_text': button_text,
#                 'user_followers': user_followers,
#                 'user_following': user_following, }
#     return render(request, 'profile.html', context)





# @login_required(login_url='signin')
# def settings(request):
#     user_profile = Profile.objects.get(user=request.user)

#     if request.method == 'POST':
#         if request.FILES.get('image') == None:
#             image = user_profile.profile_img
#             bio = request.POST['bio']
#             location = request.POST['location']

#             user_profile.profile_img = image
#             user_profile.bio = bio
#             user_profile.location = location
#             user_profile.save()

#         if request.FILES.get('image') != None:
#             image = request.FILES.get('image')
#             bio = request.POST['bio']
#             location = request.POST['location']

#             user_profile.profile_img = image
#             user_profile.bio = bio
#             user_profile.location = location
#             user_profile.save()

#         return redirect('settings')


#     return render(request, 'setting.html', {'user_profile': user_profile})

