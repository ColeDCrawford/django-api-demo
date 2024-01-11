from django.db import models

# Create your models here.

class Amendment(models.Model):
    date = models.DateField()
    text = models.TextField()
    title = models.CharField(max_length=100)

    def __str__(self):
        return self.title
    