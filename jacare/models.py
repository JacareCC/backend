from django.db import models
from django.utils import timezone

class Customer(models.Model):
    customer_uid = models.CharField(max_length=255, unique=True, blank=False)
    user_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    birthday = models.DateField(null=True)

class Restaurant(models.Model):
    place_id = models.TextField(blank=False, null=False)
    business_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    contact_person = models.CharField(max_length=200, null=True)

class CustomerReviews(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer_service_points = models.IntegerField()
    customer_service_comments = models.TextField(null=True)
    atmosphere_points = models.IntegerField()
    atmosphere_comments = models.TextField(null=True)
    accessibility_points = models.IntegerField()
    accessibility_comments = models.TextField(null=True)
    food_quality_points = models.IntegerField()
    food_quality_comments = models.TextField(null=True)
    value_for_price_points = models.IntegerField()
    value_for_price_comments = models.TextField(null=True)

    created_at = models.DateTimeField(default=timezone.now, editable=False)

    def save(self, *args, **kwargs):
        #only when create a new review 
        if not self.id:
            self.created_at = timezone.now()
        return super().save(*args, **kwargs)

class RestaurantUser(models.Model):
    restaurant_user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant_name = models.CharField()
    # restaurant_place_id = models.CharField()
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=15)
    contact_person = models.CharField(max_length=200)
    
class RestaurantsOwned(models.Model):
    restaurant_user = models.ForeignKey(RestaurantUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)