from django.shortcuts import render, get_object_or_404, redirect
from django.views import View
from accounts.models import User
from django.contrib import messages
from django.contrib.auth import logout


class ProfileView(View):
    def get(self, request, pk):
        user = get_object_or_404(User, pk=pk)
        posts = user.posts.all()

        return render(request, 'accounts/profile.html', {'user': user, 'posts': posts})


class EditProfileView(View):
    # form_class = EditUserForm

    def get(self, request):
        form = self.form_class(instance=request.user.profile, initial={'email': request.user.email})
        return render(request, 'accounts/edit_profile.html', {'form': form})

    def post(self, request):
        form = self.form_class(request.POST, instance=request.user.profile)
        if form.is_valid():
            form.save()
            request.user.email = form.cleaned_data['email']
            request.user.save()
            messages.success(request, 'profile edited successfully', 'success')
        return redirect('account:user_profile', request.user.id)


class LogoutUserView(View):
    def get(self, request):
        logout(request)
        messages.success(request, 'you logged out successfully', 'success')
        return redirect('home:home')
