from django.contrib.auth import authenticate, login
from django.http.response import HttpResponseRedirect
from django.urls import reverse
from django.shortcuts import render

from intragram.users.forms import SignUpForm


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


# request를 통해 데이터를 받고 DB에 받는 대신, 
# form을 사용하면 별도의 로직 작성 없이 form으로 묶은 후 save할 수 있다.
def signup(request):
    if request.method == 'GET':
        form = SignUpForm()
        return render(request, 'users/signup.html', {'form':form})

    elif request.method == 'POST':
        form = SignUpForm(request.POST)

        # 유효성 검사 후 저장
        if form.is_valid():
            form.save()

            # 회원가입 후 자동으로 로그인하기 위해, 저장된 데이터를 불러온다.
            user_name = form.cleaned_data['username'] # clenaed_data : 유효한 데이터가 저장됨
            user_password = form.cleaned_data['password']

            # Log-in 로직
            user = authenticate(request, username=user_name, password=user_password)

            if user is not None: # redirect to a success page
                login(request, user)
                return HttpResponseRedirect(reverse('posts:index')) # post 앱으로 redirect
            
        return render(request, 'users/main.html') # 로그인 실패시 다시 메인 페이지로
