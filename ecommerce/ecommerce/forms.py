from django import forms
from django.contrib.auth import get_user_model

User = get_user_model()

class ContactForm(forms.Form):
    fullname = forms.CharField(widget=forms.TimeInput(attrs={
                                 "class": "form-control", "id": "form_full_name", 
                                 "placeholder": "Your Full Name" }))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"class":"form-control",
                                  "placeholder": "Your valid email"  }))
    content = forms.CharField(widget=forms.Textarea(attrs={
                                    "placeholder": "Your message" }))



    # method to validate email field just for testing
    # def clean_email(self): 
    #     email = self.cleaned_data.get("email")
    #     if not "gmail.com" in email:
    #         raise forms.ValidationError("Email has to be gmail.com")
    #     return email    


















