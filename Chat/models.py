from django.db import models

# Create your models here.


class FakeNews(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    label = models.CharField(max_length=100)
    # Add other fields as needed
