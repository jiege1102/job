# job_board/forms.py

from django import forms
from .models import File,Resume,Application

class JobForm(forms.ModelForm):
    class Meta:
        model = File
        fields = ['title', 'company', 'salary', 'address', 'post', 'experience','type','demand']



class ResumeForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['full_name', 'contact_info', 'education', 'work_experience', 'skills']




class ApplicationForm(forms.ModelForm):
    class Meta:
        model = Application
        fields = ['resume']
