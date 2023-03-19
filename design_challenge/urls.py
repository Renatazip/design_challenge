from django.contrib import admin
from django.urls import path, include
from system.views import *


urlpatterns = [
    path('', include('system.urls')),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/signup/', SignUpView.as_view(), name='signup'),
    path('accounts/signup/student/', StudentSignUpView.as_view(), name='student_signup'),
    path('accounts/signup/mentor/', MentorSignUpView.as_view(), name='mentor_signup'),
]
