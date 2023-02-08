from django.contrib.auth.models import User
from .models import Profile

'''
                            - Signals -
    This will listen on saves or presaves in the application
'''
from django.db.models.signals import post_save, post_delete

'''
                            - Decorators -
    Useing decorators with the signals insted of only the signals.
'''
from django.dispatch import receiver

# Send mail functions
from django.conf import settings
from django.core.mail import send_mail

#@receiver(post_save,sender =Profile)
def createProfile(sender, instance, created, **kwargs):
    if created:
        user = instance
        profile = Profile.objects.create(
            user=user,
            username=user.username,
            email=user.email,
            name=user.first_name,
        )
        
        subject = "Welcome to IMONITCV!!"
        message = 'This is a confim mail. Thanks!! We are happy to have you onboard.'
        send_mail(
        subject,
        message,
        settings.EMAIL_HOST_USER,
        [profile.email],
        fail_silently=False,
)

#@receiver(post_save,sender =Profile)
def updateUser(sender, instance, created , **kwargs):
    #importent to add correct instance attributes.
    profile = instance
    user = profile.user
    if created == False:
        user.first_name = profile.name
        user.username = profile.username
        user.email = profile.email
        user.save()

@receiver(post_delete, sender=Profile)
def deleteUser(sender, instance, **kwargs):
    try:
        user = instance.user
        print("User is deleted...")
        user.delete()
    except User.DoesNotExist:
        print('User deletion was called from CASCADE')

'''
This is probebly the best way to use signal methods. 
But there is also a way to use decoraters. 
'''
post_save.connect(createProfile, sender=User)
post_save.connect(updateUser, sender=Profile)

'''
BUGFIX: There was a problem to delete a profile and user at once when using the 
signal method "post_delete.connect(deleteUser, sender=Profile)". 
I did try the decoration method and that worked for the delete method.
'''
#post_delete.connect(deleteUser, sender=Profile)
