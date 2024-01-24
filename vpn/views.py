from urllib.parse import urljoin

import requests
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy, reverse
from django.views import View, generic

from vpn.forms import SiteForm
from vpn.html_modificator import modify_html
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


def router_view(request, user_site_name, routes_on_original_site):
    user = request.user
    site = get_object_or_404(Site, name=user_site_name, user=user)
    original_url = urljoin(site.url, routes_on_original_site)
    response = requests.get(original_url)
    original_html = response.text
    internal_url = reverse('service:router', kwargs={'user_site_name': user_site_name,
                                                     'routes_on_original_site': routes_on_original_site})


    modified_html = modify_html(original_html, user_site_name, routes_on_original_site, request)
    return HttpResponse(modified_html)
