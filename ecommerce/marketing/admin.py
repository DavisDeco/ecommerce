from django.contrib import admin

from .models import MarketingPreference

# class that determines how model is displayed in admin ui
class MarketingPreferenceAdmin(admin.ModelAdmin):
    # details to show on main model admin ui
    list_display = ['__str__', 'subscribed', 'updated']
    # make this fields only readable not editable
    readonly_fields = ['mailchimp_msg','mailchimp_subscribed','timestamp','updated']

    class Meta:
        model = MarketingPreference
        fields = [
            'user',
            'subscribed',
            'mailchimp_msg',
            'mailchimp_subscribed',
            'timestamp',
            'updated'
        ]


# Register your models here.
admin.site.register(MarketingPreference, MarketingPreferenceAdmin)
