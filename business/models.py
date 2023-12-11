from django.db import models
from django.utils import timezone

# Create your models here.
class Restaurant(models.Model):
    place_id = models.TextField(blank=False, null=False)
    business_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    contact_person = models.CharField(max_length=200, null=True)
    retaurant_level = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    claimed = models.BooleanField()
    qr_code_link = models.CharField(null=True, default=None)
    owner_user_id = models.ForeignKey('user.User', on_delete=models.SET_NULL, null=True, blank=True)
    location = models.JSONField(default=dict)
    def __str__(self):
        return self.business_name
    
class TierReward(models.Model):
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    reward_level = models.CharField()
    reward_description = models.TextField()
    points_required = models.IntegerField()
    refresh = models.IntegerField(null=True)

class RegistrationRequests(models.Model):
    class Meta:
        verbose_name_plural = "Registration Requests"

    user_id = models.ForeignKey('user.User', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    business_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20, default='pending')
