from django.contrib import messages
from django.contrib.auth import authenticate, get_user_model, login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import redirect, render
from django.utils.http import is_safe_url
from django.views.generic import CreateView, DetailView, FormView

from .forms import GuestForm, LoginForm, RegisterForm
from .models import GuestEmail
from .signals import user_logged_in

#####################################################################
# this fuction-based view only allow logged in users to see particular page
# @login_required
# def account_home_view(request):
#     context = {}

#     return render(request,"accounts/home.html",context)


# class based login required for view using Loginrequiredmixin (same as above method)
class AccountHomeView(LoginRequiredMixin, DetailView):
    template_name = "accounts/home.html"
    def get_object(self):
        return self.request.user
         








#####################################################################
def guest_register_view(request):
    # instantiate the GuestForm
    form = GuestForm(request.POST or None)   
    args = {
        "form":form
    }
    # 
    next_ = request.GET.get('next')
    next_post = request.POST.get('next')
    redirect_path = next_ or next_post or None

    # if the form was filled and has user data
    if form.is_valid():        
        # get cleaned data and authenticate
        email = form.cleaned_data.get("email")
        # save the new guest email and send to session
        new_guest_email = GuestEmail.objects.create(email=email)
        request.session['guest_email_id'] = new_guest_email.id

        if is_safe_url(redirect_path,request.get_host()):
            return redirect(redirect_path)
        else:    
            # Redirect to a success page
            return redirect("/register/")       

    return redirect("/register/") 


#########################################################################

class LoginView(FormView):
    form_class = LoginForm
    success_url = '/'
    template_name = "accounts/login.html"

    def form_valid(self,form):
        request = self.request
         # 
        next_ = request.GET.get('next')
        next_post = request.POST.get('next')
        redirect_path = next_ or next_post or None

        # get cleaned data and authenticate
        email = form.cleaned_data.get("email")
        password = form.cleaned_data.get("password")
        user = authenticate(request,username=email,password=password)

        if user is not None:
            if not user.is_active:
                messages.error(request,"This user is inactive.")
                return super(LoginView,self).form_invalid(form)

            login(request,user)
            # send signal
            user_logged_in.send(user.__class__,instance=user,request=request)
            # delete guest session id if user logged in
            try:
                del request.session['guest_email_id']
            except:
                pass

            if is_safe_url(redirect_path,request.get_host()):
                return redirect(redirect_path)
            else:    
                return redirect("/")
        # if user is none
        return super(LoginView,self).form_invalid(form)        



#   Method based approach
# def login_page(request):
#     # instantiate the loginfform
#     form = LoginForm(request.POST or None)   
#     args = {
#         "form":form
#     }

#     # 
#     next_ = request.GET.get('next')
#     next_post = request.POST.get('next')
#     redirect_path = next_ or next_post or None

#     # if the form was filled and has user data
#     if form.is_valid():        
#         # get cleaned data and authenticate
#         username = form.cleaned_data.get("username")
#         password = form.cleaned_data.get("password")
#         user = authenticate(request,username=username,password=password)

#         if user is not None:
#             login(request,user)
#             # delete guest session id if user logged in
#             try:
#                 del request.session['guest_email_id']
#             except:
#                 pass

#             if is_safe_url(redirect_path,request.get_host()):
#                 return redirect(redirect_path)
#             else:    
#                 return redirect("/")
#         else:
#             # Return an 'invalid login' error message
#             print("Error")    

#     return render(request,"accounts/login.html",args)    

#############################################################################

class RegisterView(CreateView):
    form_class = RegisterForm 
    template_name = 'accounts/register.html'
    success_url = '/login/'

#    method based approach
# User = get_user_model() 
# def register_page(request):
#     # instantiate the loginfform
#     form = RegisterForm(request.POST or None)
#     args = {
#         "form": form
#     }
  
#     if form.is_valid():
#         form.save()

#     return render(request,"accounts/register.html",args)   