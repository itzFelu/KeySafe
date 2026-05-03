from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, SecurityQuestionForm
from .models import User

from django.contrib import messages

def signup_view(request):
    form = SignupForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()

            messages.success(request, "Account created successfully!")
            return redirect('login')
        else:
            messages.error(request, "Please fix the errors below.")

    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    form = LoginForm(request.POST or None)

    if request.method == 'POST':
        if form.is_valid():
            user = authenticate(
                request,
                email=form.cleaned_data['email'],
                password=form.cleaned_data['password']
            )

            if user:
                request.session['pre_auth_user'] = user.id
                return redirect('security-question')
            else:
                messages.error(request, "Invalid email or password")

    return render(request, 'accounts/login.html', {'form': form})


def security_question_view(request):
    user_id = request.session.get('pre_auth_user')

    if not user_id:
        messages.error(request, "Session expired. Please login again.")
        return redirect('login')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        answer = request.POST.get('answer')

        if answer.lower().strip() == user.security_answer.lower().strip():
            login(request, user)
            del request.session['pre_auth_user']
            messages.success(request, "Login successful!")
            return redirect('dashboard')
        else:
            messages.error(request, "Incorrect answer. Try again.")

    return render(request, 'accounts/security_question.html', {
        'question': user.get_security_question_display()
    })



def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


def home_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')

