from django.db import models

class News(models.Model):
    title = models.CharField(max_length=500)
    description = models.TextField(null=True, blank=True)
    category = models.CharField(max_length=500, null=True, blank=True)
    link = models.URLField(unique=True)
    image = models.URLField(null=True, blank=True)
    published_at = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.title
