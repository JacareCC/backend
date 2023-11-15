from django.db import models


class Hello(models.Model):
    message = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.message
    
