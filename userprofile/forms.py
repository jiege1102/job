from django import forms
from django.contrib.auth.models import User

class UserLoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

class UserRegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)
    role = forms.ChoiceField(choices=[('hr', 'HR'), ('job_seeker', '求职者')], widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ('username', 'email')

    def clean_password2(self):
        data = self.cleaned_data
        if data.get('password') == data.get('password2'):
            return data.get('password')
        else:
            raise forms.ValidationError("密码输入不一致，请重试。")


