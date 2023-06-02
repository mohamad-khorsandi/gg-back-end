import datetime
from django.db import models
from garden.models import Garden
from accounts.models import NormalUser
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver


class GardenScore(models.Model):
    garden = models.ForeignKey(Garden, on_delete=models.CASCADE, related_name='scores', blank=True)
    user = models.ForeignKey(NormalUser, on_delete=models.CASCADE, blank=True)
    score = models.IntegerField(default=5, validators=[MinValueValidator(0), MaxValueValidator(5)])
    comment = models.TextField(null=True, blank=True)
    date = models.DateTimeField(default=datetime.datetime.now, blank=True)

    class Meta:
        unique_together = ('garden', 'user')

    def __str__(self):
        return self.user.name


@receiver([post_save, post_delete], sender=GardenScore)
def update_garden_avg_score(sender, instance, **kwargs):
    garden = instance.garden
    scores = GardenScore.objects.filter(garden=garden)
    total_score = sum([score.score for score in scores])
    if len(scores) == 0:
        avg_score = 0.0
    else:
        avg_score = total_score / len(scores)
    garden.avg_score = avg_score
    garden.save()
