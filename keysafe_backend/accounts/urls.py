from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('security-question/', views.security_question_view, name='security-question'),
    path('logout/', views.logout_view, name='logout'),
]