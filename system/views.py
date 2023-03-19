from django.shortcuts import render, redirect
from django.views.generic import TemplateView
from django.views.generic import CreateView, ListView
from system.models import User, Student, Task, InterviewQuestion, TakenTask, TakenInterviewQuestion, Company
from system.forms import StudentSignUpForm, MentorSignUpForm, SendTask, SendInterviewQuestion
from django.utils.decorators import method_decorator
from system.decorators import student_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.db.models import Count
from django.contrib.auth import login

class SignUpView(TemplateView):
    template_name = 'registration/signup.html'


class StudentSignUpView(CreateView):
    model = Student
    form_class = StudentSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'student'
        return super().get_context_data(**kwargs)

    def form_valid(self, form):
        user = form.save()
        login(self.request, user)
        return redirect('problems')


class MentorSignUpView(CreateView):
    model = User
    form_class = MentorSignUpForm
    template_name = 'registration/signup_form.html'

    def get_context_data(self, **kwargs):
        kwargs['user_type'] = 'mentor'
        return super().get_context_data(**kwargs)


@method_decorator([login_required, student_decorator], name='dispatch')
class TasksListView(ListView):
    model = Task
    ordering = ('name',)
    template_name = 'system/student/problems_list.html'
    context_object_name = 'tasks'

    def get_queryset(self):
        student = self.request.user.student
        queryset = Task.objects.all()
        return queryset

    def get_context_data(self, *, object_list=None, **kwargs):
        context = super().get_context_data(**kwargs)
        context['companies'] = Company.objects.annotate(task_count=Count('task_company'))


        return context

@method_decorator([login_required, student_decorator], name='dispatch')
class QuestionsListView(ListView):
    model = InterviewQuestion
    ordering = ('name',)
    template_name = 'system/student/questions_list.html'
    context_object_name = 'questions'

    def get_queryset(self):
        student = self.request.user.student
        queryset = InterviewQuestion.objects.all()
        return queryset


@login_required
@student_decorator
def take_task(request, pk):
    task = get_object_or_404(Task, pk=pk)
    student = request.user.student
    took_task = TakenTask.objects.filter(task=task).filter(student=student)
    if took_task.count() == 1:
        solution = took_task.first()
        return render(request, 'system/student/take_task.html',{
            'task': task,
            'solution': solution,
            'have_solution': True,
        })
    if request.method == 'POST':
        form = SendTask(request.POST)
        if form.is_valid():
            form.instance.task = task
            form.instance.student = student
            form.instance.status = 'submitted'
            form.save()
            return redirect('problems')
        else:
            print(form.errors)
    else:
        form = SendTask()
    return render(request, 'system/student/take_task.html', {
        'form': form,
        'task': task,
        'have_solution': False,
    })


@student_decorator
def take_interview_question(request, pk):
    interview_question = get_object_or_404(InterviewQuestion, pk=pk)
    student = request.user.student
    took_interview_question = TakenInterviewQuestion.objects.filter(question=interview_question).filter(student=student)
    if took_interview_question.count() == 1:
        solution = took_interview_question.first()
        return render(request, 'system/student/take_interview_question.html',{
            'interview_question': interview_question,
            'solution': solution,
            'have_solution': True,
        })
    if request.method == 'POST':
        form = SendInterviewQuestion(request.POST)
        if form.is_valid():
            form.instance.question = interview_question
            form.instance.student = student
            form.instance.status = 'submitted'
            form.save()
            return redirect('interview_questions')
        else:
            print(form.errors)
    else:
        form = SendInterviewQuestion()

    return render(request, 'system/student/take_interview_question.html', {
        'form': form,
        'interview_question': interview_question,
        'have_solution': False,
    })
