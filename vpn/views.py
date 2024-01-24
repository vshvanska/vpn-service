import sys

import requests

from urllib.parse import urljoin
from django.contrib.auth import get_user_model
from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Count, Sum
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.urls import reverse_lazy
from django.views import View, generic
from vpn.forms import SiteForm
from vpn.html_modificator import modify_html
from vpn.models import Site, Visit
from vpn.statistics import generate_bar_chart, generate_line_chart


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
    start_page = request.META.get("HTTP_REFERER", None)
    visit = Visit(
        user=user,
        site=site,
        routes_on_original_site=routes_on_original_site,
        start_page=start_page,
    )

    original_url = urljoin(site.url, routes_on_original_site)
    response = requests.get(original_url)
    original_html = response.text
    modified_html = modify_html(
        original_html, user_site_name, routes_on_original_site
    )

    request_size = sys.getsizeof(request)
    response_size = sys.getsizeof(modified_html)

    visit.uploaded_data = request_size
    visit.downloaded_data = response_size
    visit.save()

    return HttpResponse(modified_html)


def statistics_view(request):
    user = request.user

    visit_data_transitions = (
        Visit.objects.filter(user=user)
        .exclude(start_page="http://127.0.0.1:8000/sites/")
        .values("site__name")
        .annotate(transitions=Count("id"))
    )

    labels_transitions = [
        visit["site__name"] for visit in visit_data_transitions
    ]
    values_transitions = [
        int(visit["transitions"]) for visit in visit_data_transitions
    ]

    visit_data_visits = (
        Visit.objects.filter(user=user)
        .values("site__name")
        .annotate(visits=Count("id"))
    )

    labels_visits = [visit["site__name"] for visit in visit_data_visits]
    values_visits = [int(visit["visits"]) for visit in visit_data_visits]

    upload_data = (
        Visit.objects.filter(user=user)
        .values("site__name")
        .annotate(uploads=Sum("uploaded_data"))
    )
    download_data = (
        Visit.objects.filter(user=user)
        .values("site__name")
        .annotate(downloads=Sum("downloaded_data"))
    )
    activity_data = (
        Visit.objects.filter(user=user)
        .values("datetime__date")
        .annotate(activity_count=Count("id"))
        .order_by("datetime__date")
    )

    labels_uploads = [visit["site__name"] for visit in upload_data]
    values_uploads = [visit["uploads"] for visit in upload_data]

    labels_downloads = [visit["site__name"] for visit in download_data]
    values_downloads = [visit["downloads"] for visit in download_data]

    labels_activity = [entry["datetime__date"] for entry in activity_data]
    values_activity = [entry["activity_count"] for entry in activity_data]

    chart_data_transitions = generate_bar_chart(
        labels_transitions,
        values_transitions,
        "Site Transactions statistics",
        "Site",
        "Number of transactions",
    )
    chart_data_visits = generate_bar_chart(
        labels_visits,
        values_visits,
        "Site Visits statistics",
        "Site",
        "Number of visits",
    )
    chart_data_uploads = generate_bar_chart(labels_uploads,
                                            values_uploads,
                                            "Uploads by Site",
                                            "Site",
                                            "Data, bytes")
    chart_data_downloads = generate_bar_chart(labels_downloads,
                                              values_downloads,
                                              "Downloads by Site",
                                              "Site",
                                              "Data, bytes")

    chart_data_activity = generate_line_chart(labels_activity,
                                              values_activity,
                                              "User Activity",
                                              "Date",
                                              "Activity Count")

    return render(
        request,
        "service/statistics.html",
        {
            "chart_data_transitions": chart_data_transitions,
            "chart_data_visits": chart_data_visits,
            "chart_data_uploads": chart_data_uploads,
            "chart_data_downloads": chart_data_downloads,
            "chart_data_activity": chart_data_activity,
        },
    )
