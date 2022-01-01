
from django.core.checks import messages
from django.shortcuts import get_object_or_404, redirect, render
from django.contrib import messages
from django.contrib.auth import login, logout
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail.message import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from .tokens import generate_token
from blogger.settings import EMAIL_HOST_USER
from django.core.paginator import (Paginator,PageNotAnInteger,EmptyPage)
from .models import Profile
from blog.models import Post
from .forms import UpdateProfile , UpdateImage
from django.contrib.auth.decorators import login_required

def sign_up(request):
    if request.user.is_authenticated:
        return redirect('blog:blog_home')

    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        pass1 = request.POST['pass1']
        pass2 = request.POST['pass2']

        if User.objects.filter(username=username).first():
            messages.error(request,'username has been token .. please choise anther one')
            return redirect('.')

        if User.objects.filter(email=email).exists():
            messages.error(request,'this email is aleady exist')
            return redirect('.')
        if pass1 != pass2:
            messages.error(request,'password does not match')
            return redirect('.')

        user = User.objects.create_user(username=username,email=email,password=pass1) 
        message = f'hello {user.username} \n thanks for visit our site'
        subject ='we have sent a link  an your email '
        email_sent = EMAIL_HOST_USER
        email_recive =[user.email]
        send_mail(subject,message,email_sent,email_recive,fail_silently=True)
        user.is_active=False
        user.save()

        current_site = get_current_site(request)
        email_subject = 'confirm email from @blog'
        message2 = render_to_string('user/confirm_email.html',{
            'user':user.username,
            'domain':current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            'token':generate_token.make_token(user)
        })
        email = EmailMessage(
            email_subject,
            message2,
            EMAIL_HOST_USER,
            [user.email]
        )
        email.fail_silently = True
        email.send()

        messages.success(request,'success created an account ... please check your email for activate your account')       
        return redirect('blog:blog_home')
    return render(request, 'user/sign_up.html')

def log_out(request):
    logout(request)
    return redirect('blog:blog_home')

def active(request,uidb64,token):
    try:
        # force_text
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
        if user is not None and generate_token.check_token(user,token):
            user.is_active = True
            user.save()
            login(request,user)
            return redirect('blog:blog_home')
    except:
        pass 
    return render(request,'user/faild_active.html')    

@login_required()
def profile(request,user_id):
    user_id = request.user.id
    profile = get_object_or_404(Profile,user__id=user_id)
    post = Post.objects.filter(created_by__id=user_id)
    paginator = Paginator(post,2)
    page = request.GET.get('page')
    try:
        post = paginator.page(page)
    except PageNotAnInteger:
        post = paginator.page(1)
    except EmptyPage:
        post = paginator.page(paginator.num_pages)    
    post_pag = Post.objects.filter(created_by__id=user_id)
    context = {'profile': profile, 'posts': post, 'post_pag': post_pag}

    return render(request,'user/profile.html',context)


@login_required()
def update_profile(request):
    if request.method == 'POST':
        update_user = UpdateProfile(request.POST,instance=request.user)
        update_img = UpdateImage(request.POST,request.FILES,instance=request.user.profile)
        if update_user.is_valid() and update_img.is_valid():
            update_user.save()
            update_img.save()
            messages.success(request,'success updeted ...')
            return redirect('/user/profile/' + str(request.user.id))
    else:
        update_user = UpdateProfile(instance=request.user)
        update_img = UpdateImage(instance=request.user.profile)
    context ={'update_user':update_user,'update_img':update_img}    

    return render(request,'user/update_profile.html',context)


@login_required()
def all_post_user(request,post_id):
    post_id = request.user.id
    post_user =Post.objects.filter(created_by__id=post_id)
    paginator = Paginator(post_user,2)
    page = request.GET.get('page')
    try:
        post_user = paginator.page(page)
    except PageNotAnInteger:
        post_user = paginator.page(1)
    except EmptyPage:
        post_user = paginator.page(paginator.num_pages)        
    context = {'post_user':post_user}
    return render (request,'user/all_post_user.html',context)


@login_required()
def show_post_foruser(request,post_id):
    post = get_object_or_404(Post,id=post_id)
    return render(request,'user/single_post.html',{'post':post})
