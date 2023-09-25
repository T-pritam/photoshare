from django.db.models.signals import post_save
from .models import category
from django.dispatch import receiver

@receiver(post_save,sender=category)
def postsave(sender,instance,created,**kwargs):
    print("signal is trigerd")

