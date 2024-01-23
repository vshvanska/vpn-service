from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View, generic


class ProfileView(LoginRequiredMixin, View):
    template_name = "service/profile.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    fields = ("username", "first_name", "last_name", "email")
    template_name = "service/user_form.html"
    success_url = reverse_lazy("service:profile")
