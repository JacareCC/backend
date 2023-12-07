from django.db import models
from django.utils import timezone

# Create your models here.
class User(models.Model):
    user_uid = models.CharField(max_length=255, unique=True, blank=False)
    user_name = models.CharField(max_length=100, null=True)
    birthday = models.DateField(null=True)
    level = models.IntegerField(null=True)
    date_joined = models.DateField(auto_now_add=True)
    email = models.EmailField(null=True)

    def __str__(self):
        return self.email

class UserTier(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey('business.Restaurant', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    tier = models.ForeignKey('business.TierReward', null=True, on_delete=models.CASCADE)
    
    def has_refreshed(self):
        if self.tier.refreshes_in is None:
            return True
        
        time_difference = timezone.now() - self.created_at
        refresh = self.tier.refreshes_in - timezone.now()
        return time_difference.total_seconds() >= refresh.total_seconds()

class Points(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    value = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    last_update = models.DateTimeField(auto_now=True)
    expires_at = models.DateTimeField(null=True)

class VisitedHistory(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    restaurant_id = models.ForeignKey('business.Restaurant', on_delete=models.CASCADE)
    date_visited = models.DateTimeField(auto_now_add=True)
    saved = models.BooleanField(default=False)
