from django.contrib import admin
from django.contrib.auth.models import User
from jacare.models import claim_requests, Restaurant



class claimRequestsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'business_name', 'status', )
    actions = ['approve_requests', 'reject_requests']

    readonly_fields = ('user_id', 'first_name', 'last_name', 'business_name', 'email', 'contact_person', 'address', 'phone_number')

    def approve_requests(self, request, queryset):
        queryset.update(status='approved')

    def reject_requests(self, request, queryset):
        queryset.update(status='rejected')

admin.site.register(claim_requests, claimRequestsAdmin)

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'email', 'phone_number', 'contact_person', 'retaurant_level', 'address', 'claimed', 'owner_user_id')
    list_filter = ('claimed', 'retaurant_level', 'owner_user_id')
    search_fields = ('business_name', 'email', 'phone_number', 'contact_person', 'address')
    list_editable = ('owner_user_id',) 

admin.site.register(Restaurant, RestaurantAdmin)