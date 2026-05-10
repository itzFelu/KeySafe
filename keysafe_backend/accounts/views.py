from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.shortcuts import render, redirect
from .forms import SignupForm, LoginForm, SecurityQuestionForm
from .models import User

from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode
from django.utils.encoding import force_bytes
from django.core.mail import send_mail
from django.urls import reverse
from django.utils.http import urlsafe_base64_decode

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
    try:

        user_id = request.session.get('pre_auth_user')
    except Exception as e:
        print(e)
        messages.error(request, "Something went wrong, please try again.")
        return redirect('login')


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


@require_POST
def logout_view(request):
    logout(request)
    messages.success(request, "Logged out successfully!")
    return redirect('login')


def home_redirect_view(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def profile_view(request):
    return render(request, 'accounts/profile.html')


@login_required
@require_POST
def send_password_reset_email_view(request):

    user = request.user

    uid = urlsafe_base64_encode(force_bytes(user.pk))

    token = default_token_generator.make_token(user)

    reset_link = request.build_absolute_uri(
        reverse(
            'reset-password',
            kwargs={
                'uidb64': uid,
                'token': token
            }
        )
    )

    send_mail(
        subject='KeySafe Password Reset',
        message=f'''
Hello {user.name},

Click below to reset your password:

{reset_link}
''',
        from_email=None,
        recipient_list=[user.email],
        fail_silently=False
    )

    messages.success(
        request,
        "Password reset link sent successfully."
    )

    return redirect('profile')


def forgot_password_view(request):

    if request.method == 'POST':

        email = request.POST.get('email')

        user = User.objects.filter(email=email).first()

        if user:

            uid = urlsafe_base64_encode(force_bytes(user.pk))

            token = default_token_generator.make_token(user)

            reset_link = request.build_absolute_uri(
                reverse(
                    'reset-password',
                    kwargs={
                        'uidb64': uid,
                        'token': token
                    }
                )
            )

            send_mail(
                subject='KeySafe Password Reset',
                message=f'''
Hello {user.name},

Click the link below to reset your password:

{reset_link}

If you did not request this, ignore this email.
''',
                from_email=None,
                recipient_list=[user.email],
                fail_silently=False
            )

        messages.success(
            request,
            "If an account exists, a password reset link has been sent."
        )

        return redirect('forgot-password')

    return render(request, 'accounts/forgot_password.html')


def reset_password_view(request, uidb64, token):

    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)

    except:
        user = None

    if not user or not default_token_generator.check_token(user, token):

        messages.error(request, "Invalid or expired reset link.")
        return redirect('login')

    if request.method == 'POST':

        password = request.POST.get('password')
        confirm = request.POST.get('confirm_password')

        if password != confirm:
            print("password Mismatch")
            messages.error(request, "Passwords do not match.")
            return redirect(request.path)

        user.set_password(password)
        user.save()

        messages.success(request, "Password updated successfully.")

        return redirect('login')

    return render(request, 'accounts/reset_password.html')