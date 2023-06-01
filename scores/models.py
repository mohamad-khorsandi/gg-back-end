import datetime

from django.db import models
from garden.models import Garden
from accounts.models import NormalUser
from django.core.validators import MinValueValidator, MaxValueValidator


class GardenScore(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name='scores', blank=True)
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE, blank=True)
    score = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now(), blank=True)

    class Meta:
        unique_together = ('garden', 'user')

    def __str__(self):
        return self.user.name
