from django.db import models
from business.models import Restaurant
from user.models import User

class CustomerReviews(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    data = models.JSONField(default=dict)
    email = models.EmailField()
    created_at = models.DateTimeField(auto_now_add=True)
    isVerified = models.BooleanField(default=False)







