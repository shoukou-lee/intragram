from django.contrib.auth import forms as admin_forms
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django import forms as django_forms
User = get_user_model()


class UserChangeForm(admin_forms.UserChangeForm):
    class Meta(admin_forms.UserChangeForm.Meta):
        model = User


class UserCreationForm(admin_forms.UserCreationForm):
    class Meta(admin_forms.UserCreationForm.Meta):
        model = User

        error_messages = {
            "username": {"unique": _("This username has already been taken.")}
        }

class SignUpForm(django_forms.ModelForm):
    class Meta:
        # 이메일, 이름, 유저네임, 패스워드
        model = User
        fields = ['email', 'name', 'username', 'password']

        labels = {
            'email': '이메일 주소', 
            'name' : '성명',
            'username' : '사용자 이름',
            'password' : '비밀번호'
        }
        # 패스워드 입력이 보여지지 않기 위해
        widgets = {
            'password' : django_forms.PasswordInput(),
        }

    # save 오버라이딩
    # 부모의 save함수 호출
    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password"])
        if commit: user.save()
        return user