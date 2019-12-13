from django import forms

from .models import MarketingPreference

class MarketingPreferenceForm(forms.ModelForm):
    subscribed = forms.BooleanField(label='Receive our marketing Emails?',required=False)

    class Meta:
        model = MarketingPreference
        fields = [
            'subscribed'
        ]