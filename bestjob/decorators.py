from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.models import User

def is_hr(user):
    return user.groups.filter(name='HR').exists()

def is_job_seeker(user):
    return user.groups.filter(name='Job Seeker').exists()

# 装饰器用于检查用户是否是HR
hr_required = user_passes_test(is_hr, login_url='/login/')

# 装饰器用于检查用户是否是求职者
job_seeker_required = user_passes_test(is_job_seeker, login_url='/login/')
