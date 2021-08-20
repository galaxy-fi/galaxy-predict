from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from article.models import UserInfo

def signup(request):
    if request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            user = User.objects.create_user(
                request.POST['username'], password=request.POST['password1'])
            user_info = UserInfo(user=user, rating=5.0)
            user_info.save()
            auth.login(request, user)
            return redirect('article_list')
    return render(request, 'signup.html')

def signout(request):
    auth.logout(request)
    return redirect('article_list')

def signin(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(request, username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect('article_list')
        else:
            return render(request, 'signin.html', {'error': '입력 정보가 잘못되었습니다.'})
    else:
        return render(request, 'signin.html')