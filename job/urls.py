"""job URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

import bestjob.views
import userprofile.views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('bestjob.urls')),
    re_path(r'^$', bestjob.views.job_list),
    path('login/', userprofile.views.user_login, name='login'),
    path('logout/', userprofile.views.user_logout, name='logout'),
    path('register/', userprofile.views.user_register, name='register'),
    path('apply_for_job/<int:job_id>/', bestjob.views.apply_for_job, name='apply_for_job'),
]
