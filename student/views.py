from django.shortcuts import render
from .models import UserProfile
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib import messages
from django.shortcuts import render, redirect
from django.contrib.auth import update_session_auth_hash


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

    student = UserProfile.objects.get(user=user)

    if request.method == "POST":
        if len(request.POST.get('description')) > 180 or len(request.POST.get('name')) > 20:
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
