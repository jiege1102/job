
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import Group
from .decorators import hr_required
from .forms import JobForm, ResumeForm, ApplicationForm
from .models import File, Resume, Application
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage


def job_list(request):
    query = request.GET.get('q')

    # 如果存在搜索关键字，则进行模糊查询
    if query:
        job_list = File.objects.filter(
            Q(title__icontains=query) |  # 标题包含关键字
            Q(company__icontains=query) |  # 公司名包含关键字
            Q(post__icontains=query) |  # 职位信息包含关键字
            Q(experience__icontains=query)  # 经验要求包含关键字
        )
    else:
        job_list = File.objects.all()

    paginator = Paginator(job_list, 6)  # 将查询结果分页，每页显示6条数据

    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)

    context = {
        'page': page,
        'query': query,  # 将搜索关键字传递到模板以在搜索框中显示
    }
    return render(request, 'job_list.html', context)



@hr_required
def publish_job(request):
    if request.method == 'POST':
        form = JobForm(request.POST)
        if form.is_valid():
            job = form.save(commit=False)
            job.posted_by = request.user  # 将发布者设置为当前用户
            job.save()
            return redirect('job_list')
    else:
        form = JobForm()

    return render(request, 'publish_job.html', {'form': form})

@login_required
def job_detail(request, job_id):
    job = get_object_or_404(File, pk=job_id)
    user = request.user
    applications = Application.objects.filter(job=job)

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.applicant = user
            application.job = job
            application.save()
            return redirect('job_detail', job_id=job.id)
    else:
        form = ApplicationForm(initial={'job': job})

    context = {
        'job': job,
        'form': form,
        'applications': applications,
        'type':type
    }
    return render(request, 'job_detail.html', context)





@login_required
def create_resume(request):
    user = request.user

    if request.method == 'POST':
        form = ResumeForm(request.POST)

        if form.is_valid():
            resume = form.save(commit=False)
            resume.user = user
            resume.save()
            return redirect('view_resume',resume_id=resume.id)
    else:
        form = ResumeForm()

    return render(request, 'create_resume.html', {'form': form})

@login_required
def view_resume(request, resume_id):
    resume = get_object_or_404(Resume, pk=resume_id)
    return render(request, 'view_resume.html', {'resume': resume})


@login_required
def apply_for_job(request, job_id):
    job = File.objects.get(pk=job_id)
    user = request.user

    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            application = form.save(commit=False)
            application.job = job  # 关联到招聘信息
            application.applicant = user  # 关联到求职者
            application.save()
            return redirect('job_list')
    else:
        form = ApplicationForm(initial={'job': job})

    return render(request, 'apply_for_job.html', {'job': job, 'form': form})

def view_applications(request, job_id):
    job = File.objects.get(pk=job_id)
    applications = Application.objects.filter(job=job)

    return render(request, 'view_applications.html', {'job': job, 'applications': applications})


def profile(request):
    if request.user.is_authenticated:
        if request.user.groups.filter(name='HR').exists():
            # 如果用户是HR，重定向到HR个人中心
            return redirect('hr_profile')
        else:
            # 否则，重定向到求职者个人中心
            return redirect('job_seeker_profile')
    else:
        # 如果用户未登录，可以在这里添加适当的处理
        return redirect('login')  # 或者显示一个登录页面

@login_required
def hr_profile(request):
    if request.user.groups.filter(name='HR').exists():
        # 如果用户是 HR，获取该 HR 创建的工作列表
        jobs = File.objects.filter(posted_by=request.user)

        context = {
            'jobs': jobs,
        }

        return render(request, 'hr_profile.html', context)
    else:
        # 如果用户不是 HR，重定向到个人中心页面
        return redirect('profile')


@login_required
def job_seeker_profile(request):
    user = request.user
    applications = Application.objects.filter(applicant=user)
    try:
        resume = Resume.objects.get(user=user)
    except Resume.DoesNotExist:
        resume = None

    return render(request, 'job_seeker_profile.html', {'applications': applications, 'resume': resume})

