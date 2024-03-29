from django.contrib import admin
from business.models import RegistrationRequests, Restaurant

# Register your models here.
class RegistrationRequestsAdmin(admin.ModelAdmin):
    list_display = ('user_id', 'business_name', 'status')
    actions = ['approve_requests', 'reject_requests']

    def approve_requests(self, request, queryset):
        queryset.update(status='approved')
        for request_obj in queryset:
            self.process_approval(request_obj)

    def reject_requests(self, request, queryset):
        queryset.update(status='rejected')

    def process_approval(self, request_obj):
        if request_obj.status == 'approved':
            business_name = request_obj.business_name.strip().lower()
            try:
                restaurant = Restaurant.objects.get(business_name__iexact=business_name)
                restaurant.owner_user_id = request_obj.user_id
                restaurant.claimed = True
                restaurant.qr_code_link = f"https://quickchart.io/qr?text=http%3A%2F%2Fjacareview.com%3A3000%2Frestaurants%2Frewards%3Fid%3D{restaurant.id}&size=200¢erImageUrl=https%3A%2F%2Fwww.jacareview.com%2F_next%2Fimage%3Furl%3D%252F_next%252Fstatic%252Fmedia%252Flogo-home--.135443cd.png%26w%3D1080%26q%3D75"
                restaurant.save()
            except Restaurant.DoesNotExist:
                print(f"No matching restaurant found for business name: {business_name}")
            return
            

admin.site.register(RegistrationRequests, RegistrationRequestsAdmin)

class RestaurantAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'claimed', 'owner_user_id')
    list_filter = ('claimed', 'retaurant_level', 'owner_user_id')
    search_fields = ('business_name', 'email', 'phone_number', 'contact_person', 'address')
    list_editable = ('owner_user_id', 'claimed') 

admin.site.register(Restaurant, RestaurantAdmin)