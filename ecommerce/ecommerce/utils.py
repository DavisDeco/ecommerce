from django.utils.text import slugify
import random
import string

def random_string_generator(size=10,chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def unique_key_generator(instance):
    # """
    # This is for a Django project and it assumes your instance has a model with a key field
    # """    
    size = random.randint(30,45)
    key = random_string_generator(size=size)
    
    Klass = instance.__class__
    try:
        qs_exists = Klass.objects.filter(key=key).exits()
        if qs_exists: 
            return unique_slug_generator(instance)
    except:
        return key 
        
    return key 


def unique_order_id_generator(instance):
    # """
    # This is for a Django project and it assumes your instance has a model with a order_id field
    # """    

    order_new_id = random_string_generator()
    
    Klass = instance.__class__
    try:
        qs_exists = Klass.objects.filter(order_id=order_id).exits()
        if qs_exists: 
            return unique_slug_generator(instance)
    except:
        return order_new_id 
        
    return order_new_id 



def unique_slug_generator(instance, new_slug=None):
    # """
    # This is for a Django project and it assumes your instance has a model with a slug field
    # and a title character (char) field
    # """    

    if new_slug is not None:
        slug = new_slug
    else:
        slug = slugify(instance.title)

    Klass = instance.__class__
    qs_exists = Klass.objects.filter(slug=slug).exits()
    if qs_exists:
        new_slug = "{slug}-{randstr}".format(
                    slug=slug,
                    randstr=random_string_generator(size=4)
                ) 
        return unique_slug_generator(instance,new_slug=new_slug)  
    return slug     