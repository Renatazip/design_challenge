from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.html import escape, mark_safe


class User(AbstractUser):
    is_student = models.BooleanField(default=False)
    is_mentor = models.BooleanField(default=False)

class Company(models.Model):
    name = models.CharField(max_length=255)
    logo = models.ImageField(upload_to='company_logo', null=True, blank=True)

    def __str__(self):
        return self.name

class Task(models.Model):
    LEVELS = (
        ('easy', 'easy'),
        ('medium', 'medium'),
        ('hard', 'hard'),
    )
    name = models.CharField(max_length=255)
    description_design = models.CharField(max_length=255)
    description_for = models.CharField(max_length=255)
    description_to_help = models.CharField(max_length=255)
    level = models.CharField(max_length=255, choices=LEVELS, default='easy')
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name='task_company', blank=True, null=True)

    def __str__(self):
        return self.name

class InterviewQuestion(models.Model):
    LEVELS = (
        ('easy', 'easy'),
        ('medium', 'medium'),
        ('hard', 'hard'),
    )
    question = models.CharField(max_length=255,)
    level = models.CharField(max_length=255, choices=LEVELS, default='easy')

class Student(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, primary_key=True)
    tasks = models.ManyToManyField(Task, through="TakenTask")

class TakenTask(models.Model):
    STATUSES =[
        ('exist', 'exist',),
        ('open', 'open',),
        ('submitted', 'submitted',),
        ('reviewed', 'reviewed',),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_tasks')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='taken_tasks')
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=256, choices=STATUSES, default='open')
    text_answer = models.TextField(default='')
    review = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.task.name + ' - ' + self.text_answer

class AnswerToTask(models.Model):
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_answers')
    task = models.ForeignKey(Task, on_delete=models.CASCADE, related_name='task_answers')
    date = models.DateTimeField(auto_now_add=True)
    text_answer = models.TextField()

    def __str__(self):
        return self.text_answer

class TakenInterviewQuestion(models.Model):
    STATUSES = [
        ('exist', 'exist',),
        ('open', 'open',),
        ('submitted', 'submitted',),
        ('reviewed', 'reviewed',),
    ]
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='taken_question')
    question = models.ForeignKey(InterviewQuestion, on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=256, choices=STATUSES, default='open')
    text_answer = models.TextField(default='')
    review = models.TextField(default='', null=True, blank=True)

    def __str__(self):
        return self.text_answer