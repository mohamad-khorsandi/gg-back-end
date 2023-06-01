import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('accounts', '0001_initial'),
        ('plants', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Garden',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('phone_number', models.CharField(max_length=11, validators=[django.core.validators.MinLengthValidator(11)])),
                ('business_code', models.CharField(max_length=12, validators=[django.core.validators.MinLengthValidator(12)])),
                ('address', models.TextField()),
                ('avg_score', models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(0.0), django.core.validators.MaxValueValidator(5.0)])),
                ('location', models.URLField(blank=True, null=True)),
                ('profile_photo', models.ImageField(blank=True, null=True, upload_to='')),
                ('is_verified', models.BooleanField(default=False)),
                ('garden_owner', models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='accounts.gardenownerprofile')),
                ('plants', models.ManyToManyField(blank=True, to='plants.plant')),
            ],
        ),
    ]
