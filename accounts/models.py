from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager


class UserManager(BaseUserManager):

    def create_user(self, phone_number, email, name, password):
        if not phone_number:
            raise ValueError('user must have phone number')

        if not email:
            raise ValueError('user must have email')

        if not name:
            raise ValueError('user must have = name')

        user = self.model(phone_number=phone_number, email=self.normalize_email(email), name=name)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, phone_number, email, name, password):
        user = self.create_user(phone_number, email, name, password)
        user.is_admin = True
        user.is_staff = True
        user.save(using=self._db)
        return user


class User(AbstractUser):
    name = models.CharField(max_length=100)
    email = models.EmailField(max_length=255, unique=True)
    phone_number = models.CharField(max_length=11, unique=True)

    # override AbstractUser fields
    objects = UserManager()
    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['phone_number', 'name']
    username = None

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True


class TemporaryUser(models.Model):
    email = models.EmailField(max_length=255, unique=True)
    code = models.PositiveSmallIntegerField()
    created = models.DateTimeField(auto_now=True)
    name = models.CharField(max_length=100)
    password = models.CharField(max_length=128)
    phone_number = models.CharField(max_length=11, unique=True)

    def __str__(self):
        return f'{self.email} - {self.code} - {self.created}'

    @classmethod
    def from_clean_data(cls, cd, random_code):
        return TemporaryUser(email=cd['email'], phone_number= cd['phone_number'], name=cd['name'], password=cd['password'], code=random_code)

    def to_user(self) -> User:
        return User(email=self.email, phone_number=self.phone_number, name=self.name, password=self.password)

