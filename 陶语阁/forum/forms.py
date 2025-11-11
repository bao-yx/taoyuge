from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User,Post,Category,Tag
from django.contrib.auth.forms import AuthenticationForm

# 登录表单
class LoginForm(AuthenticationForm):
    pass

# 注册表单
class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)  # 可选：添加邮箱字段

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')  # 注册字段

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        if commit:
            user.save()
        return user

class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'category', 'tags', 'image']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

