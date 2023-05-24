from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator


# Create your models here.
class Plant(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    fragrance = models.BooleanField()
    type = models.CharField(max_length=50)
    light_intensity = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(3)])
    temperature = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(2)])
    location_type = models.CharField(max_length=50)
    water_need = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])
    growth = models.IntegerField()
    pet_compatible = models.BooleanField()
    allergy_compatible = models.BooleanField()
    attention_need = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(7)])
    edible = models.BooleanField()
    wikipedia_link = models.URLField()
    special_condition = models.TextField()
    main_image = models.ImageField()
    season = models.PositiveIntegerField(default=1, validators=[MinValueValidator(1), MaxValueValidator(4)])
    is_seasonal = models.BooleanField(default=False)

    def __str__(self):
        return self.name
