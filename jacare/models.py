from django.db import models
from django.utils import timezone

class User(models.Model):
    user_uid = models.CharField(max_length=255, unique=True, blank=False)
    user_name = models.CharField(max_length=100, null=True)
    birthday = models.DateField(null=True)
    level = models.IntegerField(null=True)
    date_joined = models.DateField(auto_now_add=True)

class Restaurant(models.Model):
    place_id = models.TextField(blank=False, null=False)
    business_name = models.CharField(max_length=100, null=True)
    email = models.EmailField(unique=True, null=True)
    phone_number = models.CharField(max_length=15, null=True)
    contact_person = models.CharField(max_length=200, null=True)
    retaurant_level = models.IntegerField(null=True)
    address = models.CharField(max_length=200, null=True)
    claimed = models.BooleanField()
    owner_user_id = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.title

class CustomerReviews(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    data = models.JSONField(default=dict)
    created_at = models.DateTimeField(auto_now_add=True)
    isVerified = models.BooleanField(default=False)

class Tier(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    level = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True)

class TierReward(models.Model):
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    reward_level = models.IntegerField()
    reward_description = models.TextField()
    refresh = models.IntegerField()
    points_required = models.IntegerField()

class Points(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True)

class visited_history(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    date_visited = models.DateTimeField(auto_now_add=True)
    saved = models.BooleanField(default=False)

class claim_requests(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    business_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    contact_person = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    phone_number = models.CharField(max_length=15)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return self.title