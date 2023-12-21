from django.db import models
from business.models import Restaurant
from user.models import User

class CustomerReviews(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    data = models.JSONField(default=dict)
    email = models.EmailField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    isVerified = models.BooleanField(default=False)
    isHidden = models.BooleanField(default=False)

class CheckinHistory(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    check_in_date = models.DateField(auto_now_add=True)




