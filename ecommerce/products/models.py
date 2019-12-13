import os
import random
from django.db import models
from django.db.models import Q
from django.db.models.signals import pre_save, post_save
from django.urls import reverse


from ecommerce.utils import unique_slug_generator


def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext

def upload_image_path(instance, filename):
    # print(instance)
    # print(filename)
    new_filename = random.randint(1,3910209341)
    name, ext = get_filename_ext(filename)
    final_filename = '{new_filename}{ext}'.format(new_filename=new_filename,ext=ext)

    return "products/{new_filename}/{final_filename}".format(
                                                            new_filename=new_filename,
                                                            final_filename=final_filename
                                                            )    

# create a custom query set to override the default
class ProductQuerySet(models.query.QuerySet):
    def featured(self):
        return self.filter(featured=True)

    def active(self):
        return self.filter(active=True) 

    def search(self,query): 
        lookups = ( Q(title__icontains=query) |
                    Q(description__icontains=query) |
                    Q(price__icontains=query) |
                    Q(tag__title__icontains=query)
                  )
        return self.filter(lookups).distinct()



# this is a product model manager
class ProductManager(models.Manager):
    def get_queryset(self):
        return ProductQuerySet(self.model,using=self._db)

    
    def all(self):
        return self.get_queryset().active()
    
    def features(self):
        return self.get_queryset().featured()


    def get_by_id(self,id):
        qs = self.get_queryset().filter(id=id)
        if qs.count() == 1:
            return qs.first()
        return None

    def search(self,query):  
        return self.get_queryset().active().search(query)  


# Product model
class Product(models.Model):
    title = models.CharField(max_length=120)
    slug = models.SlugField(unique=True)
    description = models.TextField()
    price = models.DecimalField(decimal_places=2, max_digits=20,default=0.00)
    image = models.ImageField(upload_to=upload_image_path ,null=True,blank=True)
    featured = models.BooleanField(default=False)
    active = models.BooleanField(default=True)
    timestamp = models.DateTimeField(auto_now_add=True)

    # extend product manager 
    objects = ProductManager()

    # this method creats a link to display details of a product using pk
    def get_absolute_url(self):
        # return "/products/{pk}".format(pk=self.pk)
        return reverse("products:detail",kwargs={"pk":self.pk})
    



    # this method will display details on admin site
    def __str__(self):
        return self.title

# create receiver for slug generator
def product_pre_save_receiver(sender,instance,*args,**kwargs):
    if not instance.slug:
        instance.slug = unique_slug_generator(instance)

# activate pre-save with generated slug
pre_save.connect(product_pre_save_receiver, sender=Product)        