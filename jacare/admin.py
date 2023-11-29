from django.contrib import admin
from django.contrib.auth.models import User
from jacare.models import claim_requests



class claimRequestsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'business_name', 'status', )
    actions = ['approve_requests', 'reject_requests']

    readonly_fields = ('user_id', 'first_name', 'last_name', 'business_name', 'email', 'contact_person', 'address', 'phone_number')

    def approve_requests(self, request, queryset):
        queryset.update(status='approved')

    def reject_requests(self, request, queryset):
        queryset.update(status='rejected')

admin.site.register(claim_requests, claimRequestsAdmin)
