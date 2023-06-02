from django.db import models


class Plant(models.Model):
    LIGHT_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    TEMPERATURE_CHOICES = [
        (1, 'Warm'),
        (2, 'Sultry'),
    ]
    WATER_CHOICES = [
        (1, 'Everyday'),
        (2, 'Each two day'),
        (3, 'Once a week'),
        (4, 'Each two weeks'),
    ]
    PLANT_CHOICES = [
        (1, 'Prickly'),
        (2, 'With Flower'),
        (3, 'Flowerless'),
    ]
    LOCATION_TYPE_CHOICES = [
        (1, 'Apartment'),
        (2, 'Close'),
        (3, 'Open'),
    ]
    GROWTH_CHOICES = [
        (1, 'Seed'),
        (2, 'Sapling'),
        (3, 'Complete'),
    ]
    ATTENTION_NEED_CHOICES = [
        (1, 'Everyday'),
        (2, 'Weekly'),
        (3, 'Monthly'),
    ]
    SEASON_CHOICES = [
        (1, 'Spring'),
        (2, 'Summer'),
        (3, 'Fall'),
        (4, 'Winter'),
    ]
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    maintenance = models.TextField(null=True, blank=True)
    type = models.PositiveIntegerField(default=1, choices=PLANT_CHOICES)
    light_intensity = models.PositiveIntegerField(default=1, choices=LIGHT_CHOICES)
    temperature = models.PositiveIntegerField(default=1, choices=TEMPERATURE_CHOICES)
    location_type = models.PositiveIntegerField(default=1, choices=LOCATION_TYPE_CHOICES)
    water = models.PositiveIntegerField(default=1, choices=WATER_CHOICES)
    growth = models.PositiveIntegerField(default=1, choices=GROWTH_CHOICES)
    attention_need = models.PositiveIntegerField(default=1, choices=ATTENTION_NEED_CHOICES)
    season = models.PositiveIntegerField(default=1, choices=SEASON_CHOICES)
    is_valid = models.BooleanField(default=False)
    is_seasonal = models.BooleanField(default=False)
    fragrance = models.BooleanField()
    pet_compatible = models.BooleanField()
    allergy_compatible = models.BooleanField()
    edible = models.BooleanField()
    special_condition = models.TextField(null=True, blank=True)
    wikipedia_link = models.URLField(null=True, blank=True)
    main_img = models.ImageField(upload_to='static/plants/main_images/', default=None, null=True, blank=True)

    def __str__(self):
        return self.name


class PlantImage(models.Model):
    img = models.ImageField(upload_to='static/plants/images/')
    plant = models.ForeignKey(Plant, on_delete=models.CASCADE, related_name='images')
