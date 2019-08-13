from django.db import models


# Create your models here.
class Actions(models.Model):
    urls = models.TextField(max_length=1000, blank=False, null=False)
    email = models.EmailField()
    timestamp = models.DateTimeField(auto_now_add=True, auto_now=False)

    def __str__(self):
        return str(self.timestamp)
