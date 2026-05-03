from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, SecurityQuestionForm
from .models import User

def signup_view(request):
    form = SignupForm(request.POST or None)

    if form.is_valid():
        user = form.save(commit=False)
        user.set_password(form.cleaned_data['password'])
        user.save()
        login(request, user)
        return redirect('dashboard')

    return render(request, 'accounts/signup.html', {'form': form})



def login_view(request):
    form = LoginForm(request.POST or None)

    if form.is_valid():
        user = authenticate(
            request,
            email=form.cleaned_data['email'],
            password=form.cleaned_data['password']
        )

        if user:
            request.session['pre_auth_user'] = user.id
            return redirect('security-question')

    return render(request, 'accounts/login.html', {'form': form})


def security_question_view(request):
    user_id = request.session.get('pre_auth_user')

    if not user_id:
        return redirect('login')

    user = User.objects.get(id=user_id)

    if request.method == 'POST':
        answer = request.POST.get('answer')

        if answer == user.security_answer:
            login(request, user)
            del request.session['pre_auth_user']
            return redirect('dashboard')

    return render(request, 'accounts/security_question.html', {
        'question': user.get_security_question_display()
    })

