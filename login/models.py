from django.db import models

# Create your models here.
from django.db import models

class Report(models.Model):
    reporter_name = models.CharField(max_length=100)
    reporter_email = models.EmailField()
    reporter_ph = models.CharField(max_length=15, blank=True, null=True)  # Optional
    news_title = models.TextField(default="Nothing")
    news_description = models.TextField()
    news_url = models.URLField(blank=True, null=True)  # Optional

    def __str__(self):
        return f"{self.reporter_name} - {self.news_description[:20]}"
