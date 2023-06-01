from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

from plants.models import Plant


class UserManager(BaseUserManager):
    def create_user(self, name, email, password, phone_number=None):
        user = self.model(name=name, email=email, phone_number=phone_number)  # todo normalize email
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, name, email, password, phone_number=None):
        user = self.create_user(name=name, email=email, password=password, phone_number=phone_number)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class NormalUser(AbstractUser):

    LIGHT_CHOICES = [
        (1, 'Low'),
        (2, 'Medium'),
        (3, 'High'),
    ]
    LOCATION_TYPE_CHOICES = [
        (1, 'Apartment'),
        (2, 'Close'),
        (3, 'Open'),
    ]
    ATTENTION_NEED_CHOICES = [
        (1, 'Everyday'),
        (2, 'Weekly'),
        (3, 'Monthly'),
    ]


    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, null=True, blank=True)
    is_garden_owner = models.BooleanField(default=False)
    image = models.ImageField(null=True, blank=True, upload_to='static/users/')
    saved_plants = models.ManyToManyField(Plant, blank=True)
    light_condition = models.PositiveIntegerField(null=True, default=None, choices=LIGHT_CHOICES)
    location_type_condition = models.PositiveIntegerField(null=True, default=None, choices=LOCATION_TYPE_CHOICES)
    attention_need = models.PositiveIntegerField(null=True, default=None, choices=ATTENTION_NEED_CHOICES)
    have_pet = models.BooleanField(null=True, default=None)
    have_allergy = models.BooleanField(null=True, default=None)

    # override AbstractUser fields
    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['name']
    first_name = None
    last_name = None
    username = None

    def __str__(self):
        return self.email


# -----------------------------------------------------------------------------------------
class GardenOwnerManger(BaseUserManager):
    def get_queryset(self, *args, **kwargs):
        queryset = super().get_queryset(*args, **kwargs)
        queryset = queryset.filter(is_garden_owner=True)
        return queryset


class GardenOwnerProfile(models.Model):
    user = models.OneToOneField(NormalUser, on_delete=models.CASCADE)
    national_id = models.IntegerField(null=True, blank=True)
    business_id = models.IntegerField(null=True, blank=True)
    license = models.ImageField(upload_to='garden_license_pics', null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def __str__(self):
        return self.user.email


class GardenOwner(NormalUser):
    class Meta:
        proxy = True

    objects = GardenOwnerManger()

    def save(self, *args, **kwargs):
        self.is_garden_owner = True
        return super().save(*args, **kwargs)


@receiver(post_save, sender=GardenOwner)
def garden_owner_creator(sender, instance, created, **kwargs):
    if created and instance.is_garden_owner:
        GardenOwnerProfile.objects.create(user=instance)
# -----------------------------------------------------------------------------------------


class TemporaryUser(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=11, unique=True)
    is_garden_owner = models.BooleanField(default=False)

    def __str__(self):
        return f'{self.email} - {self.code} - {self.created} - {self.is_garden_owner}'

    @classmethod
    def from_clean_data(cls, cd, random_code):
        return TemporaryUser(email=cd['email'], phone_number= cd['phone_number'],
                             name=cd['name'], password=cd['password'], code=random_code,
                             is_garden_owner=cd['is_garden_owner'])

    def to_user(self):
        if self.is_garden_owner:
            return GardenOwner(email=self.email, phone_number=self.phone_number, name=self.name, password=self.password)
        else:
            return NormalUser(email=self.email, phone_number=self.phone_number, name=self.name, password=self.password)

