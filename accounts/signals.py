from django.db.models.signals import pre_save,post_save
from .models import User,UserProfile
from django.dispatch import receiver

@receiver(post_save,sender=User)
def post_save_create_profile_receiver(sender,instance,created,**kwargs):

  if created:
    UserProfile.objects.create(user=instance)
  else:
    try:
      profile = UserProfile.objects.get(user=instance)
      profile.save()
    except:
      UserProfile.objects.create(user=instance)

@receiver(pre_save,sender=User)
def pre_save_profile_receiver(sender,instance,**kwargs):
  pass
