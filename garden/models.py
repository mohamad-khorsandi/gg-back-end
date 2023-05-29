from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator, MinLengthValidator, MaxLengthValidator


class Garden(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(max_length=11, validators=[MinLengthValidator(11)])
    business_code = models.CharField(max_length=12, validators=[MinLengthValidator(12)])
    address = models.TextField()
    avg_score = models.FloatField(default=0.0, validators=[MinValueValidator(0.0), MaxValueValidator(5.0)])
    location = models.URLField(null=True, blank=True)
    profile = models.ImageField(null=True, blank=True)

    def __str__(self):
        return self.name
