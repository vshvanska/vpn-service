from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View, generic

from vpn.forms import SiteForm
from vpn.models import Site


class ProfileView(LoginRequiredMixin, View):
    template_name = "service/profile.html"

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)


class UserUpdateView(LoginRequiredMixin, generic.UpdateView):
    model = get_user_model()
    fields = ("username", "first_name", "last_name", "email")
    template_name = "service/user_form.html"
    success_url = reverse_lazy("service:profile")


class SiteListView(LoginRequiredMixin, generic.ListView):
    model = Site
    template_name = "service/site_list.html"
    context_object_name = "site_list"

    def get_queryset(self):
        return (Site.objects.filter(user=self.request.user)
                .select_related("user"))


class SiteCreateView(LoginRequiredMixin, generic.CreateView):
    model = Site
    form_class = SiteForm
    template_name = "service/site_form.html"
    success_url = reverse_lazy("service:site-list")

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)
