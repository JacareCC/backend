from django.contrib import admin
from business.models import RegistrationRequests, Restaurant

# Register your models here.
class RegistrationRequestsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'business_name', 'status', )
    actions = ['approve_requests', 'reject_requests']

    readonly_fields = ('user_id', 'first_name', 'last_name', 'business_name', 'email', 'contact_person', 'address', 'phone_number')

    def approve_requests(self, request, queryset):
        queryset.update(status='approved')

    def reject_requests(self, request, queryset):
        queryset.update(status='rejected')

admin.site.register(RegistrationRequests, RegistrationRequestsAdmin)

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'email', 'phone_number', 'contact_person', 'retaurant_level', 'address', 'claimed', 'owner_user_id')
    list_filter = ('claimed', 'retaurant_level', 'owner_user_id')
    search_fields = ('business_name', 'email', 'phone_number', 'contact_person', 'address')
    list_editable = ('owner_user_id',) 

admin.site.register(Restaurant, RestaurantAdmin)