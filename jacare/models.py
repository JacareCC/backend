from django.db import models
from django.utils import timezone

class Customer(models.Model):
    customer_uid = models.CharField(max_length=255, unique=True)
    user_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birthday = models.DateField()

class Restaurant(models.Model):
    place_id = models.TextField()
    business_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    contact_person = models.CharField(max_length=200)

class CustomerReviews(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    customer_service_points = models.IntegerField()
    customer_service_comments = models.TextField()
    atmosphere_points = models.IntegerField()
    atmosphere_comments = models.TextField()
    accessibility_points = models.IntegerField()
    accessibility_comments = models.TextField()
    food_quality_points = models.IntegerField()
    food_quality_comments = models.TextField()
    value_for_price_points = models.IntegerField()
    value_for_price_comments = models.TextField()

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