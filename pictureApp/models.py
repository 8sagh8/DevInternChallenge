from django.db import models

# Create your models here.

class Photo(models.Model):
    title = models.CharField(max_length=50, default="Not Available")
    image = models.ImageField()
    status = models.BooleanField(default=True)
    
    def __str__(self):
        return self.title + ' status: ' + str(self.status)