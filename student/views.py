from .forms import SignupForm
from .models import UserProfile

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.http import HttpResponse
from django.contrib.auth import login, authenticate

from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core.exceptions import ObjectDoesNotExist


def index(request):
    students = UserProfile.objects.all()
    context_list = []
    for student in students:
        context_list.append({
            'name': student.displayed_name,
            'description': student.description,
            'photo_url': student.photo_url,
            'redirect_url': student.redirect_url
        })
    context_list.sort(key= lambda k: k["name"])

    return render(request, 'student/index.html', {'context_list': context_list})

@login_required
def my(request):
    user = request.user
    try:
        student = UserProfile.objects.get(user=user)
    except ObjectDoesNotExist:
        userprofile = UserProfile()
        userprofile.user = user
        userprofile.redirect_url="http://www.sinfstudent.be"
        userprofile.photo_url = "https://gladstoneentertainment.com/wp-content/uploads/2018/05/avatar-placeholder.gif"
        userprofile.displayed_name = user.first_name + " " + user.last_name
        userprofile.save()
        student = UserProfile.objects.get(user=user)

    if request.method == "POST":
        if len(request.POST.get('description')) > 120 or len(request.POST.get('name')) > 20:
            messages.error(request, 'There are some error in your answer')
        else:
            student.description = request.POST.get('description')
            student.displayed_name = request.POST.get('name')
            student.photo_url = request.POST.get('photo_url')
            student.redirect_url = request.POST.get('redirect')
            student.save()
            messages.add_message(request, messages.SUCCESS, 'Profile Updated !')

    information = {
        'name': student.displayed_name,
        'description': student.description,
        'photo_url': student.photo_url,
        'redirect_url': student.redirect_url
    }
    return render(request, 'student/my.html', information)


@login_required
def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.add_message(request, messages.SUCCESS, 'Password changed')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/change_password.html', {
        'form': form
    })


def signup(request):
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            current_site = get_current_site(request)
            mail_subject = 'Sinfstudent Account Activation'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'student/blank.html', {'title': "Check your email",
                                                          'type': "alert-success",
                                                          'message': "Please confirm your email address to complete the registration"})
    else:
        if request.user.is_authenticated:
            return redirect("my")
        form = SignupForm()
    return render(request, 'registration/signup.html', {'form': form})


def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        messages.add_message(request, messages.SUCCESS, 'Account activated ! Please fill in your information')

        return redirect('my')
    else:
        return render(request, 'student/blank.html', {'title': "Invalid Link", 'type': 'alert-danger', 'message': 'Invalid or expired link'})
