"""
URL configuration for service project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from vpn.views import (
    ProfileView,
    UserUpdateView,
    SiteListView,
    SiteCreateView,
    router_view,
    statistics_view,
    SiteDeleteView,
)

urlpatterns = [
    path("", ProfileView.as_view(), name="profile"),
    path("users/update/<int:pk>", UserUpdateView.as_view(), name="user-update"),
    path("sites/", SiteListView.as_view(), name="site-list"),
    path("sites/create/", SiteCreateView.as_view(), name="site-create"),
    path("sites/delete/<int:pk>", SiteDeleteView.as_view(), name="site-delete"),
    path(
        "<str:user_site_name>/<path:routes_on_original_site>/",
        router_view,
        name="router",
    ),
    path("statistics/", statistics_view, name="statistics"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

app_name = "service"
