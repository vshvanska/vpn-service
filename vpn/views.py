from django.shortcuts import render
from django.views import View


class ProfileView(View):
    template_name = 'service/profile.html'

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name)
