from datetime import datetime
from tkinter.filedialog import SaveAs
from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class category(models.Model):
    name = models.CharField(max_length=100, null=False, blank=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)

    def __str__(self):
        return self.name

class Photo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,null=True)
    category = models.ForeignKey(category, on_delete=models.CASCADE ,null=True, blank=True)
    image = models.ImageField(null=False, blank=False)
    description = models.TextField()
    uploaddate = models.DateTimeField(default=datetime.now)
    review = models.IntegerField(default=0)

    def __str__(self):
        return self.user.username

    # class Meta:
    #     ordering = ['image']

class Review(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE,null=True)
    Cat = models.ForeignKey(category, on_delete=models.CASCADE,null=True)
    review = models.IntegerField(default=0)

    def __str__(self):
        return self.review