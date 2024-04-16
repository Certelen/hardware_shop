import django.contrib.auth as auth
# import (
#     LoginView,
#     LogoutView,
#     PasswordChangeView,
#     PasswordResetView,
#     PasswordChangeDoneView,
#     PasswordResetDoneView,
#     PasswordResetConfirmView,
#     PasswordResetCompleteView
# )
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.urls import reverse_lazy
from django.http import JsonResponse

from .forms import CreationForm, UpdateUserForm
from .models import CustomUser


def signup(request):
    if request.method == "POST":
        form = CreationForm(data=request.POST)
        if not form.is_valid():
            context = {
                'signup_form': form
            }
            return render(request, 'auth/signup.html', context)
        new_user = form.save()
        auth.login(request, new_user)
        return JsonResponse(status=200, data={'login': True})
    return reverse_lazy('products:index')


def login(request):
    if request.method == "POST":
        form = auth.forms.AuthenticationForm(data=request.POST)
        if not form.is_valid():
            context = {
                'login_form': form
            }
            return render(request, 'auth/login.html', context)
        auth.login(request, form.get_user())
        return JsonResponse(status=200, data={'login': True})
    return reverse_lazy('products:index')


@login_required
def profile(request):
    if request.method == "POST":
        form = UpdateUserForm(
            request.POST, instance=CustomUser.objects.get(id=request.user.id))
        if form.is_valid():
            form = form.save(commit=False)
            form.save()
            if (request.POST['password1'] and
                    request.POST['password1'] == request.POST['password2']):
                new_password = request.POST['password1']
                user = CustomUser.objects.get(email=request.user.email)
                user.set_password(new_password)
                user.save()
            return JsonResponse(status=200, data={'update': True})
        print(request.POST)
        context = {
            'profile_form': form
        }
        return render(request, 'user/profile.html', context)
    return reverse_lazy('products:index')


@login_required
def orders(request):
    pass


@login_required
def cart(request):
    pass


@login_required
def favorite(request):
    pass
