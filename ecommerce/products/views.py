# from urllib import request

from django.core.exceptions import MultipleObjectsReturned
from django.http import Http404, request
from django.shortcuts import get_object_or_404, render
# from django.views import ListViewfrom django.http import Http404
from django.views.generic import DetailView, ListView

from carts.models import Cart
from .models import Product
from analytics.mixins import ObjectViewedMixin
# from analytics.signals import object_viewed_signal

#############################################

class ProductFeaturedListView(ListView):
    # queryset = Product.objects.all()
    template_name = "products/list.html"

    def get_queryset(self,*args,**kwargs):
        request = self.request
        return Product.objects.all().featured()



class ProductFeaturedDetailView(ObjectViewedMixin,DetailView):
    queryset = Product.objects.all().featured()
    template_name = "products/featured-detail.html"

    # def get_queryset(self,*args,**kwargs):
    #     request = self.request
    #     obj =  Product.objects.featured()
    #     print(obj)
    #     return obj

# def product_features_detail_view(request,pk=None,*args,**kwargs):    
#     # obj = Product.objects.get_by_id(pk)
#     obj = Product.objects.featured()
#     print(obj)
#     if obj is None:
#         raise Http404("No featured Products")

#     args = {
#         'obj': obj
#     }    

#     return render(request, "products/featured-detail.html",args)
   



###############################################

class ProductListView(ListView):
    queryset = Product.objects.all()
    template_name = "products/list.html"

    # in listview the context data will autonatically be held in a variable called 'object_list'

    # def get_context_data(self,*args,**kwargs):
    #     context = super(ProductListView,self).get_context_data(*args,**kwargs)
    #     print(context)
    #     return 
    def get_context_data(self,*args,**kwargs):
        context = super(ProductListView,self).get_context_data(*args,**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_queryset(self,*args,**kwargs):
        request = self.request
        return Product.objects.all()




# this method achieves the same outcome as the listview class above
def product_list_view(request):
    qs = Product.objects.all()
    args = {
        'object_list': qs
    }    

    return render(request, "products/product_list.html",args)



################### Detail Slug View ##########
class ProductDetailSlugView(ObjectViewedMixin,DetailView):
    queryset = Product.objects.all()
    template_name = "products/detail.html"

    def get_context_data(self,*args,**kwargs):
        context = super(ProductDetailSlugView,self).get_context_data(*args,**kwargs)
        cart_obj, new_obj = Cart.objects.new_or_get(self.request)
        context['cart'] = cart_obj
        return context

    def get_object(self, *args,**kwargs):
        request = self.request
        slug = self.kwargs.get('slug')
        

        # obj = get_object_or_404(Product,slug=slug,active = True)

        try:
            obj = Product.objects.get(slug=slug,active=True)
            print(obj)
        except Product.DoesNotExist:
            raise Http404("Product not found")
        except Product.MultipleObjectsReturned:
            qs = Product.objects.filter(slug=slug,active=True)
            obj = qs.first()
            print(obj)
        except:
            raise Http404 ("Oooops!!")

        #send an analytics of viewed object
        # object_viewed_signal.send(obj.__class__,instance=instance,request=request)
        return obj

##################### Detail view ####################
class ProductDetailView(ObjectViewedMixin,DetailView):
    queryset = Product.objects.all()
    template_name = "products/detailview.html"
    

    # in listview the context data will autonatically be held in a variable called 'object_list'

    def get_context_data(self,*args,**kwargs):
        context = super(ProductDetailView,self).get_context_data(*args,**kwargs)
        print(context)
        print("From context")
        return context
        
        

    def get_object(self, *args,**kwargs):
        request = self.request
        pk = self.kwargs.get('pk')

        obj = Product.objects.get_by_id(pk)
        if obj is None:
            raise Http404("Product doesn't exist")
        return obj

    # def get_queryset(self,*args,**kwargs):
    #     request = self.request
    #     pk = self.kwargs.get('pk')
    #     obj =  Product.objects.filter(pk=pk) 
    #     return obj
    #     print(obj)   






# this method achieves the same outcome as the DetailView class above
def product_detail_view(request,pk=None,*args,**kwargs):
    # obj = Product.objects.get(pk=pk)
    # obj = get_object_or_404(Product,pk=pk)

    # #first approach ######
    # try:
    #     obj = Product.objects.get(id=pk)
    # except Product.DoesNotExist:
    #     print('No product here')
    #     raise Http404("Product doesn't exist")
    # except:
    #     print("Yes! Found product")
     
    # # second approach ###### 
    # qs = Product.objects.filter(id=pk)
    # if qs.exists() and qs.count() == 1:
    #     obj = qs.first()
    # else:
    #     raise Http404("Product doesn't exist again")

    # Third approach using product manager ####
    obj = Product.objects.get_by_id(pk)
    if obj is None:
        raise Http404("Product doesn't exist from product manager")

    args = {
        'obj': obj
    }    

    return render(request, "products/detail.html",args)
