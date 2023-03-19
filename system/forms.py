from django.contrib.auth.forms import UserCreationForm
from system.models import User, Student, TakenTask, TakenInterviewQuestion
from django.db import transaction
from django import forms

class MentorSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_mentor = True
        if commit:
            user.save()
        return user

class StudentSignUpForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User

    @transaction.atomic
    def save(self, commit=True):
        user = super().save(commit=False)
        user.is_student = True
        user.save()
        student = Student.objects.create(user=user)
        return user

class SendTask(forms.ModelForm):
    class Meta:
        model = TakenTask
        fields = ['text_answer']

class SendInterviewQuestion(forms.ModelForm):
    class Meta:
        model = TakenInterviewQuestion
        fields = ['text_answer']

