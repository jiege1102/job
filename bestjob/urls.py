from django.urls import path
from . import views
urlpatterns = [
    path('list/', views.job_list, name='job_list'),
    path('publish_job/', views.publish_job, name='publish_job'),
    path('job/<int:job_id>/', views.job_detail, name='job_detail'),
    path('create_resume/', views.create_resume, name='create_resume'),
    path('view_resume/<int:resume_id>/', views.view_resume, name='view_resume'),
    path('profile/', views.profile, name='profile'),
    path('hr_profile/', views.hr_profile, name='hr_profile'),  # HR 个人中心
    path('job_seeker_profile/', views.job_seeker_profile, name='job_seeker_profile'),  # 求职者个人中心
    path('apply_for_job/<int:job_id>/', views.apply_for_job, name='apply_for_job'),
    path('view_applications/<int:job_id>/', views.view_applications, name='view_applications'),

]