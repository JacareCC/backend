from django.db import models

class Hello(models.Model):
    message = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.message

class Customer(models.Model):
    customer_uid = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    birthday = models.DateField()

class CustomerReviews(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    restaurant_id = models.IntegerField()
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

class RestaurantUser(models.Model):
    restaurant_user_uid = models.CharField(max_length=255, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    
class Restaurant(models.Model):
    business_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    phone_number = models.CharField(max_length=15)
    contact_person = models.CharField(max_length=200)

class RestaurantsOwned(models.Model):
    restaurant_user = models.ForeignKey(RestaurantUser, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)