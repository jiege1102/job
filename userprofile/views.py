from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from .forms import UserLoginForm, UserRegisterForm
from django.contrib.auth.models import Group  # 导入Group模型

# 用户登录
def user_login(request):
    if request.method == 'POST':
        user_login_form = UserLoginForm(data=request.POST)
        if user_login_form.is_valid():
            data = user_login_form.cleaned_data
            user = authenticate(username=data['username'], password=data['password'])
            if user:
                login(request, user)
                return redirect("job_list")
            else:
                return HttpResponse("账号或密码输入有误，请重新输入。")
        else:
            return HttpResponse("账号或密码输入不合法")
    elif request.method == 'GET':
        user_login_form = UserLoginForm()
        context = {'form': user_login_form}
        return render(request, 'login.html', context)
    else:
        return HttpResponse("请使用GET或POST请求数据")


def user_register(request):
    if request.method == 'POST':
        user_register_form = UserRegisterForm(request.POST)
        if user_register_form.is_valid():
            new_user = user_register_form.save(commit=False)
            password = user_register_form.cleaned_data['password']
            new_user.set_password(password)
            new_user.save()

            # 根据用户选择的角色，将其添加到相应的用户组中
            role = user_register_form.cleaned_data['role']
            if role == 'hr':
                group_name = 'HR'
            elif role == 'job_seeker':
                group_name = 'Job Seeker'
            else:
                group_name = None

            if group_name:
                group = Group.objects.get(name=group_name)
                new_user.groups.add(group)

            login(request, new_user)
            return redirect("job_list")
        else:
            return render(request, 'register.html', {'form': user_register_form})
    else:
        user_register_form = UserRegisterForm()

    return render(request, 'register.html', {'form': user_register_form})


# 用户退出
def user_logout(request):
    logout(request)
    return redirect("job_list")