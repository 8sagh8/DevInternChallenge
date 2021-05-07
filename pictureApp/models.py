from django.db import models

# Create your models here.

class Photo(models.Model):
    title = models.CharField(max_length=50, default="Not Available")
    image = models.ImageField()
    status = models.BooleanField(default=True)
    user = models.CharField(max_length=15, default="AnonymousUser")
    
    def __str__(self):
        return self.title + ' status: ' + str(self.status)