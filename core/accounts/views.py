from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, get_object_or_404, redirect
from django.views import View

from accounts.forms import UserRegistrationForm, UserLoginForm

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout, get_user_model
from .models import Profile
from django.views.generic import UpdateView
from django.urls import reverse_lazy

User = get_user_model()


class ProfileView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        posts = user.posts.all()

        return render(request, 'accounts/profile.html', {'user': user, 'posts': posts})


# class EditProfileView(View):
#     form_class = EditUserForm
#
#     def get(self, request):
#         profile = Profile.objects.get(user=request.user)
#         form = self.form_class(instance=profile)
#         return render(request, 'accounts/edit_profile.html', {'form': form})
#
#     def post(self, request):
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             form.save()
#             # request.user.email = form.cleaned_data['email']
#             request.user.save()
#             messages.success(request, 'profile edited successfully', 'success')
#         return redirect('account:user_profile', request.user.id)

class EditProfileView(LoginRequiredMixin, UpdateView):
    model = Profile
    fields = ['first_name', 'last_name', 'description', 'image']
    template_name = 'accounts/edit_profile.html'

    # success_url = reverse_lazy('accounts:user_profile')

    def get_object(self):
        return Profile.objects.get(user=self.request.user)

    def get_success_url(self):
        return reverse_lazy('accounts:user_profile', args=[self.object.user.id])


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('blog:post-list')


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:post-list')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['email'], cd['password1'])
            messages.success(request, 'you registered successfully', 'success')
            return redirect('blog:post-list')
        return render(request, self.template_name, {'form': form})


class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'

    def setup(self, request, *args, **kwargs):
        self.next = request.GET.get('next')
        return super().setup(request, *args, **kwargs)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('blog:post-list')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you logged in successfully', 'success')
                if self.next:
                    return redirect(self.next)
                return redirect('blog:post-list')
            messages.error(request, 'username or password is wrong', 'warning')
        return render(request, self.template_name, {'form': form})
