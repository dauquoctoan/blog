from django.contrib.auth.models import User
from django.shortcuts import render, get_object_or_404
from . import models
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.core.paginator import Paginator
import re

category = models.PostCategory.objects.all()


def index(request):
    postall = models.Post.objects.all()
    paginator = Paginator(postall, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/index.html', {'page_obj': page_obj, 'category': category})


def getpostbycategory(request, pk):
    postbyctegory = models.Post.objects.filter(category_id=pk)
    paginator = Paginator(postbyctegory, 2)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'pages/index.html', {'category': category, 'page_obj': page_obj})


def register(request):
    return render(request, 'pages/register.html', {'category': category})


def adduser(request):
    if request.method == 'POST':
        username = request.POST['user']
        email = request.POST['email']
        password1 = request.POST['password1']
        password2 = request.POST['password2']

        if username != '' and email != '' and password1 != '' and password1 != '':
            if not re.search('^\w+$', username):
                message_u = 'Tên tài khoản có kí tự đặc biệt'
                return render(request, 'pages/register.html', {'msg_u': message_u, 'category': category})
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                if not re.search('^[\w]{3,20}@[A-Za-z]{3,10}.[A-Za-z]{3,10}$', email):
                    message_e = 'email không hợp lệ'
                    return render(request, 'pages/register.html', {'msg_e': message_e, 'category': category})
                if password1 == password2:
                    user = User.objects.create_user(username=username, email=email, password=password1)
                    user.save()
                    return HttpResponseRedirect('/')
                else:
                    message_w = 'Mật khẩu không khớp'
                    return render(request, 'pages/register.html',
                                  {'msg_w': message_w, 'category': category})
            message_u = 'Tài khoản đã tồn tại'
            return render(request, 'pages/register.html', {'msg_u': message_u, 'category': category})
        message = 'Phải nhập đầy đủ thông tin'
    return render(request, 'pages/register.html', {'msg_u': message, 'category': category})


def post(request, pk):
    post = get_object_or_404(models.Post, pk=pk)
    if request.method == "POST":
        body = request.POST['body']
        comment = models.Comment(author=request.user, post=post, body=body)
        comment.save()
        return HttpResponseRedirect(request.path)
    return render(request, "blog/content.html", {'post': post, 'category': category})


def loginuser(request):
    next = request.POST.get('next', '/')
    return render(request, "pages/login.html", {'next': next, 'category': category})

def authuser(request):
    if request.method == "POST":
        username = request.POST['user']
        password = request.POST['password']
        next = request.POST['next']
        if username != '' and password != '':
            try:
                User.objects.get(username=username)
            except User.DoesNotExist:
                message_u = 'Tài khoản không tồn tại!'
                return render(request, 'pages/login.html', {'next': next, 'msg_u': message_u, 'category': category})
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return HttpResponseRedirect(next)
            else:
                message_w = 'Mật khẩu không đúng!'
                return render(request, 'pages/login.html', {'next': next, 'msg_w': message_w, 'category': category})
        else:
            message = 'Phải nhập đầy đủ thông tin'
            return render(request, 'pages/login.html', {'next': next, 'msg_u': message, 'category': category})

    return HttpResponseRedirect('/')
