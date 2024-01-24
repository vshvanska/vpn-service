from django.conf import settings
from django.db import models


class Site(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="schemas"
    )
    name = models.CharField(max_length=64)
    url = models.URLField()

    class Meta:
        unique_together = ["user", "url", "name"]

    def __str__(self) -> str:
        return self.name


class Visit(models.Model):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="visits"
    )
    site = models.ForeignKey(Site, on_delete=models.CASCADE)
    start_page = models.URLField()
    datetime = models.DateTimeField(auto_now_add=True)
    uploaded_data = models.BigIntegerField(default=0)
    downloaded_data = models.BigIntegerField(default=0)
    routes_on_original_site = models.TextField()

    def __str__(self) -> str:
        return f"{self.datetime} {self.site.url}"
