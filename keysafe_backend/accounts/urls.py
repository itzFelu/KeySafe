from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_redirect_view, name='home'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('security-question/', views.security_question_view, name='security-question'),
    path('logout/', views.logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path(
        'send-password-reset-email/',
        views.send_password_reset_email_view,
        name='send-password-reset-email'
    ),
    path(
        'forgot-password/',
        views.forgot_password_view,
        name='forgot-password'
    ),
    path(
        'reset-password/<uidb64>/<token>/',
        views.reset_password_view,
        name='reset-password'
    ),
    path(
        'update-security-question/',
        views.update_security_question_view,
        name='update-security-question'
    ),
]