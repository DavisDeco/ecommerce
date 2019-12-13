from random import randint

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.core.mail import send_mail
from django.db import models
from django.db.models.signals import post_save, pre_save
from django.template.loader import get_template

from ecommerce.utils import random_string_generator, unique_key_generator

######################################### Custom User Model Functionality ###########

class UserManager(BaseUserManager):
    def create_user(self,email,full_name=None,password=None,is_active = True, is_staff=False,is_admin=False):
        if not email:
            raise ValueError("Users must have an email address")
        if not password:
            raise ValueError("Users must have a password")
        # if not full_name:
        #     raise ValueError("Users must have a full name")

        user_obj = self.model(
            email = self.normalize_email(email),
            full_name = full_name
        )  

        user_obj.set_password(password) #this method can also be used to  change password  
        user_obj.active = is_active
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.save(using=self._db)
        return user_obj

    def create_staffuser(self, email,full_name=None,password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True
        )
        return user  

    def create_superuser(self, email,full_name=None,password=None):
        user = self.create_user(
            email,
            full_name=full_name,
            password=password,
            is_staff=True,
            is_admin=True
        )
        return user

class User(AbstractBaseUser):
    email = models.EmailField(max_length=255,unique=True)
    full_name = models.CharField(max_length=255,blank=True,null=True)
    active = models.BooleanField(default=True) #can login
    is_active = models.BooleanField(default=True) #can login
    staff = models.BooleanField(default=False) #staff user/ non superuser
    admin = models.BooleanField(default=False) #superuser
    timestamp = models.DateTimeField(auto_now_add=True)

    USERNAME_FIELD = 'email' #default username
    # 
    REQUIRED_FIELDS =[]

    # link to UserManager
    objects = UserManager() 

    def __str__(self):
        return self.email

    def get_full_name(self):
        if self.full_name:
            return self.full_name
        return self.email

    def get_short_name(self):
        return self.email
    
    def has_perm(self,perm,obj=None):
        return True

    def has_module_perms(self, app_label):
        return True 

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    # @property
    # def is_active(self):
    #     return self.active   
    # 
     
######################################### EMAIL activation model ###################
class EmailActivation(models.Model):
    user = models.ForeignKey(User)
    email = models.EmailField()
    key = models.CharField(max_length=120,blank=True,null=True)
    activated = models.BooleanField(default=False)
    forced_expired = models.BooleanField(default=False)
    expires = models.IntegerField(default=7) # 7 Days
    timestamp = models.DateTimeField(auto_now_add=True)
    update = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.email

    def regenerate(self):
        self.key = None
        self.save()
        if self.key is not None:
            return True
        return False
    
    def send_activation(self):
        if not self.activated and not self.forced_expired:
            if self.key:
                base_url = getattr(settings,'BASE_URL','https://yourlivedomainurl.com')
                key_path = self.key # use reverse
                path = "{base}{path}".format(base=base_url,path=key_path)
                context = {
                    'path': path,
                    'email': self.email
                }
                # get the templates and pass context
                txt_ = get_template("registration/emails/verify.txt").render(context)
                html_ = get_template("registration/emails/verify.html").render(context)
                subject = "1-Click Email Verification"
                from_email = settings.DEFAULT_FROM_EMAIL
                recipient_list = [self.email]
        
                sent_mail = send_mail(
                    subject,
                    txt_,
                    from_email,
                    recipient_list,
                    html_message=html_,
                    fail_silently=False,
                )
                return sent_mail 

            return False
# 
def pre_save_email_activation(sender,instance,*args,**kwaargs):
    if not instance.activated and not instance.forced_expired:
        if not instance.key:
            instance.key = unique_key_generator(instance)

pre_save.connect(pre_save_email_activation,sender=EmailActivation)

# 
def post_save_user_create_receiver(sender,instance,created,*args,**kwaargs):
    if created:
        obj = EmailActivation.objects.create(user=instance, email=instance.email)
        obj.send_activation()

post_save.connect(post_save_user_create_receiver,sender=User)

######################################### GuestEmail Functionality ################
class GuestEmail(models.Model):
    email = models.EmailField()
    active = models.BooleanField(default=True)
    update = models.DateTimeField(auto_now=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email  