from django.db import models

from django.contrib.auth.models import Group, User

# 创建HR组
hr_group, created = Group.objects.get_or_create(name='HR')

# 创建求职者组
job_seeker_group, created = Group.objects.get_or_create(name='Job Seeker')


class File(models.Model):
    title = models.CharField(max_length=255)
    company = models.CharField(max_length=255)
    salary = models.CharField(max_length=255)
    address = models.CharField(max_length=50)
    post = models.CharField(max_length=255)
    experience = models.CharField(max_length=255)
    demand = models.CharField(max_length=255,default="")
    type = models.CharField(max_length=255,default="")
    posted_by = models.ForeignKey(User, on_delete=models.CASCADE)

class Resume(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    # 添加简历的字段，例如姓名、联系方式、教育背景、工作经验、技能等
    full_name = models.CharField(max_length=255)
    contact_info = models.CharField(max_length=255)
    education = models.TextField()
    work_experience = models.TextField()
    skills = models.TextField()


class Application(models.Model):
    job = models.ForeignKey(File, on_delete=models.CASCADE)  # 与工作信息关联
    applicant = models.ForeignKey(User, on_delete=models.CASCADE)  # 投递简历的求职者
    # resume = models.FileField(upload_to='resumes/')  # 上传的简历文件
    resume = models.ForeignKey(Resume, on_delete=models.CASCADE, blank=True, null=True)  # 与用户关联的简历
    application_date = models.DateTimeField(auto_now_add=True)  # 投递日期