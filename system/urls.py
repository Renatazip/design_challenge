from django.contrib import admin
from django.urls import path, include
from system.views import TasksListView, take_task, QuestionsListView, take_interview_question
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
    path('admin/', admin.site.urls),
    # path('home/', name='home'),
    path('problems/', TasksListView.as_view(), name='problems'),
    path('problems/<int:pk>/', take_task, name='problem'),
    path('interview/', QuestionsListView.as_view(), name='interview_questions'),
    path('interview/<int:pk>', take_interview_question, name='interview_question'),
    # path('mentors/', name='mentors'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
