from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render


def main(request):
    # 일반적으로 페이지를 보기 위한 경우, GET을 요청
    if request.method == 'GET':
        return render(request, 'users/main.html')
    
    # 로그인의 경우, POST를 요청 - https://docs.djangoproject.com/en/3.2/topics/auth/default/
    elif request.method == 'POST':
        # POST로 받은 username/password를 저장하고 auth한다.
        user_name = request.POST['username']
        user_password = request.POST['password']
        user = authenticate(request, username=user_name, password=user_password)

        if user is not None: # redirect to a success page
            login(request, user)
            return HttpResponseRedirect(reverse('posts:index')) # post 앱으로 redirect
        else: # invalid login 
            return render(request, 'users/main.html') # 로그인 실패시 다시 메인 페이지로
