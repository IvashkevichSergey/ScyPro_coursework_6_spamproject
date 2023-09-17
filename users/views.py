from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.urls import reverse, reverse_lazy
from django.views.generic import CreateView, UpdateView, ListView

from config import settings
from users.forms import UserRegisterForm, UserProfileForm
from users.models import User


class RegisterView(CreateView):
    """Контроллер для регистрации нового пользователя"""
    model = User
    form_class = UserRegisterForm
    template_name = 'users/register.html'

    def get_success_url(self):
        return reverse('users:verify_email', args=[self.object.pk])

    def form_valid(self, form):
        self.object = form.save()
        if form.is_valid():
            verification_code = self.object.verification_code
            send_mail(
                    subject=f'Подтверждение регистрации',
                    message=f'Для подтверждения электронной почты введите на сайте следующий код:\n{verification_code}',
                    recipient_list=[self.object.email],
                    from_email=settings.EMAIL_HOST_USER,
                )
            print('EMAIL SENT')
        return super().form_valid(form)


class ProfileView(UpdateView):
    """Контроллер для отображения страницы профиля пользователя"""
    model = User
    form_class = UserProfileForm
    success_url = reverse_lazy('users:profile')

    def get_object(self, queryset=None):
        return self.request.user


def verify_email(request, pk):
    if request.method == 'GET':
        messages.success(request=request, message='Введите проверочный код, высланный на Вашу электронную почту')
    if request.method == 'POST':
        check_code = request.POST['check_code']
        user = User.objects.get(pk=pk)
        verification_code = user.verification_code
        if check_code == verification_code:
            user.is_active = True
            user.save()
            return redirect('users:login')
        else:
            messages.error(request=request, message='Введён некорректный код')
            return render(request, 'users/verify_email.html')
    return render(request, 'users/verify_email.html')


class UserListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = User
    permission_required = 'users.view_user'

    def get_queryset(self):
        queryset = super().get_queryset()
        queryset = queryset.filter(is_superuser=False, is_staff=False)
        queryset = queryset.order_by('pk')
        return queryset


def toggle_user_status(request, pk):
    user = get_object_or_404(User, pk=pk)
    if user.is_active:
        user.is_active = False
    else:
        user.is_active = True
    user.save()
    return redirect('spam:users_list')
