from django.shortcuts import render , redirect , get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.models import User , auth
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from itertools import chain
from .models import Profile , Post , LikePost , FollowersCount

# Create your views here.
@login_required(login_url='signin')
def index(request):
    user_object = get_object_or_404(User, username=request.user.username)

    user_profile = get_object_or_404(Profile, user=user_object)
    posts = Post.objects.all()
    user_following_list = []
    feed = []

    user_following = FollowersCount.objects.filter(follower = request.user.username)

    for users in user_following:
        user_following_list.append(users.user)
    for usernames in user_following_list:
        feed_lists = Post.objects.filter(user=usernames)
        feed.append(feed_lists)
    feed_list =list(chain(*feed))
        
    return render(request, 'core/index.html', {'user_profile': user_profile , 'posts':feed_list})
    

def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email = email).exists():
                messages.info(request , 'Email Taken Already')
                return redirect('signup')
            elif User.objects.filter(username = username).exists():
                messages.info(request ,'Username Taken Already')
                return redirect ('signup')
            else:
                user = User.objects.create_user(username=username , email= email , password= password)
                user.save()

                #logging user in and redirecting to settings page
                login_user = auth.authenticate(username = username , password = password)
                auth.login(request, login_user)

                #Creating Profile object for the new user
                user_model = User.objects.get(username = username)
                new_profile = Profile.objects.create(user = user_model , id_user = user_model.id)
                new_profile.save()
                return redirect('settings')
        else:
            messages.info(request , "Password Not Matched")
            return redirect ('signup')
    else:
        return render(request , 'core/signup.html' )
    
def signin(request):

    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username = username , password = password)

        if user is not None:
            auth.login(request , user)
            return redirect('home')
        else:
            messages.info(request , 'Credentials Invalid')
            return redirect('signin')
    return render(request , 'core/signin.html')

@login_required(login_url = 'signin')
def logout(request):
    auth.logout(request)
    return redirect('signin')

@login_required(login_url = 'signin')
def settings(request):
    user_profile = get_object_or_404(Profile , user=request.user)


    if request.method == 'POST':
        
        if request.FILES.get('image') == None:
            image = user_profile.profileimg
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        if request.FILES.get('image') != None:
            image = request.FILES.get('image')
            bio = request.POST['bio']
            location = request.POST['location']

            user_profile.profileimg = image
            user_profile.bio = bio
            user_profile.location = location
            user_profile.save()
        
        return redirect('settings')
    return render(request, 'core/settings.html', {'user_profile': user_profile})

def upload(request):

    if request.method == 'POST':
        user = request.user.username
        image = request.FILES.get('image_upload')
        caption = request.POST['caption']
        new_post = Post.objects.create(user = user , image=image , caption=caption)
        new_post.save()
        return redirect('home')
    else:
        return redirect('home') 
@login_required(login_url = 'signin')
def like_post(request):
    username = request.user.username
    post_id = request.GET.get('post_id')
    post = Post.objects.get(id = post_id)
    like_filter=LikePost.objects.filter(post_id=post_id , username=username).first()

    if like_filter == None:
        new_like = LikePost.objects.create(post_id=post_id , username=username)
        new_like.save()
        post.no_of_likes = post.no_of_likes+1
        post.save()
        return redirect('/')
    else:
        like_filter.delete()
        post.no_of_likes = post.no_of_likes-1
        post.save()
        return redirect('/')

@login_required(login_url = 'signin')
def profile(request,pk):
    user_object = User.objects.get(username=pk)
    user_profile = Profile.objects.get(user=user_object)
    user_posts = Post.objects.filter(user=pk)
    user_posts_length = len(user_posts)
    follower = request.user.username
    user = pk
    if  FollowersCount.objects.filter(follower = follower , user = user).first():
        button_text = 'Unfollow'
    else:
        button_text = 'Follow'

    user_followers = len(FollowersCount.objects.filter(user=pk))
    user_following= len(FollowersCount.objects.filter(follower=pk))
    context = {
        'user_object':user_object,
        'user_profile':user_profile,
        'user_posts':user_posts,
        'user_posts_length':user_posts_length,
        'button_text':button_text,
        'user_followers':user_followers,
        'user_following':user_following,

    }
    return render(request,'core/profile.html',context)

@login_required(login_url = 'signin')
def follow(request):
    if request.method=='POST':
        follower = request.POST['follower']
        user = request.POST['user']
        if FollowersCount.objects.filter(follower = follower , user=user).first():
            delete_follower = FollowersCount.objects.get(follower = follower , user= user)
            delete_follower.delete()
            return redirect('/profile/'+user)
        else:
            new_follower  =FollowersCount.objects.create(follower=follower , user=user)
            new_follower.save()
            return redirect ('/profile/'+user)
        return redirect('/')
    
@login_required(login_url = 'signin')
def search(request):
    user_object = User.objects.get(username=request.user.username)
    user_profile = Profile.objects.get(user=user_object)

    if request.method == 'POST':
        username = request.POST['username']
        username_object = User.objects.filter(username__icontains=username)

        username_profile = []
        username_profile_list = []

        for users in username_object:
            username_profile.append(users.id)

        for ids in username_profile:
            profile_lists = Profile.objects.filter(id_user=ids)
            username_profile_list.append(profile_lists)
        
        username_profile_list = list(chain(*username_profile_list))
    return render(request, 'core/search.html', {'user_profile': user_profile, 'username_profile_list': username_profile_list})