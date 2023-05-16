from django.db import models


# Create your models here.
class Plants(models.Model):
    name = models.CharField(max_length=50, null=False, blank=False)
    description = models.TextField(null=True, blank=True)
    maintenance = models.CharField(max_length=50, null=False, blank=False)
    fragrance = models.BooleanField()
    type = models.CharField(max_length=50)
    light_intensity = models.CharField(max_length=50)
    temperature = models.CharField(max_length=50)
    location_type = models.CharField(max_length=50)
    water_need = models.IntegerField()
    growth = models.IntegerField()
    pet_compatible = models.BooleanField()
    allergy_compatible = models.BooleanField()
    attention_need = models.IntegerField()
    edible = models.BooleanField()
    wikipedia_link = models.URLField()
    special_condition = models.TextField()
    main_image = models.ImageField()

    def __str__(self):
        return self.name
