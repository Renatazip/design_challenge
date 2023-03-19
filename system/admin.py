from django.contrib import admin
from system.models import User, Student, Task, Company, TakenTask, InterviewQuestion, TakenInterviewQuestion



admin.site.register(User)
admin.site.register(Student)
admin.site.register(Task)
admin.site.register(InterviewQuestion)
admin.site.register(Company)
admin.site.register(TakenTask)
admin.site.register(TakenInterviewQuestion)

