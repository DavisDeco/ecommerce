from django import forms
from .models import Address

# now we use ModelForm instead of Forms
class AddressForm(forms.ModelForm):
    class Meta:
        model = Address
        fields = [
            #'billing_profile',
            # 'address_type',
            'address_line_1',
            'address_line_2',
            'city',
            'area',
            'country',
            'postal_code'

        ]


