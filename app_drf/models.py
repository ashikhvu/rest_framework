from django.db import models
from django.contrib.auth.models import AbstractUser
from shortuuid.django_fields import ShortUUIDField
from django.db.models.signals import post_save

# Create your models here.
class ProductModel(models.Model):
    name = models.CharField(max_length=255,blank=True,null=True)
    price = models.FloatField(blank=True,null=True)

    def __str__(self):
        return self.name
    
class User(AbstractUser):
    username = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255,null=True,blank=True)
    phone = models.CharField()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
    
    def save(self,*args,**kwargs):
        email_username ,mobile = self.email.split('@')
        if self.full_name == '' or self.full_name == None:
            self.full_name = email_username
        if self.username == '' or self.username == None:
            self.username = email_username
        super(User,self).save(*args,**kwargs)

class ProfileModel(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE,blank=True,null=True)
    image = models.FileField(upload_to='images/',default='/images/profile3d.png',blank=True,null=True)
    full_name = models.CharField(max_length=255,blank=True,null=True)
    about = models.TextField(blank=True,null=True)
    gender = models.CharField(max_length=100,blank=True,null=True)
    country = models.CharField(max_length=255,blank=True,null=True)
    state = models.CharField(max_length=255,blank=True,null=True)
    city = models.CharField(max_length=255,blank=True,null=True)
    address = models.CharField(max_length=255,blank=True,null=True)
    date = models.DateTimeField(auto_now_add=True)
    pid = ShortUUIDField(unique=True,length=10,max_length=20,alphabet='abcdefghijk')

    def __str__(self):
        if self.full_name:
            return str(self.full_name)
        else:
            return str(self.user.full_name)
        
    def save(self,*args,**kwargs):
        if self.full_name == '' or self.full_name == None:
            self.full_name = self.user.full_name
        super(ProfileModel,self).save(*args,**kwargs)

def create_user_profile(sender,instance,created,**kwargs):
    if created:
        ProfileModel.objects.create(
            user=instance
        )

def save_user_profile(sender,instance,**kwargs):
    if hasattr(instance,'profile'):
        instance.profile.save()

post_save.connect(create_user_profile,sender=User)
post_save.connect(save_user_profile,sender=User)