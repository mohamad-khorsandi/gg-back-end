
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Plant',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
                ('description', models.TextField(blank=True, null=True)),
                ('maintenance', models.TextField(blank=True, null=True)),
                ('type', models.PositiveIntegerField(choices=[(1, 'Prickly'), (2, 'With Flower'), (3, 'Flowerless')], default=1)),
                ('light_intensity', models.PositiveIntegerField(choices=[(1, 'Low'), (2, 'Medium'), (3, 'High')], default=1)),
                ('temperature', models.PositiveIntegerField(choices=[(1, 'Warm'), (2, 'Sultry')], default=1)),
                ('location_type', models.PositiveIntegerField(choices=[(1, 'Apartment'), (2, 'Close'), (3, 'Open')], default=1)),
                ('water', models.PositiveIntegerField(choices=[(1, 'Everyday'), (2, 'Each two day'), (3, 'Once a week'), (4, 'Each two weeks')], default=1)),
                ('growth', models.PositiveIntegerField(choices=[(1, 'Seed'), (2, 'Sapling'), (3, 'Complete')], default=1)),
                ('attention_need', models.PositiveIntegerField(choices=[(1, 'Everyday'), (2, 'Weekly'), (3, 'Monthly')], default=1)),
                ('season', models.PositiveIntegerField(choices=[(1, 'Spring'), (2, 'Summer'), (3, 'Fall'), (4, 'Winter')], default=1)),
                ('is_valid', models.BooleanField(default=False)),
                ('is_seasonal', models.BooleanField(default=False)),
                ('fragrance', models.BooleanField()),
                ('pet_compatible', models.BooleanField()),
                ('allergy_compatible', models.BooleanField()),
                ('edible', models.BooleanField()),
                ('special_condition', models.TextField(blank=True, null=True)),
                ('wikipedia_link', models.URLField(blank=True, null=True)),
                ('main_img', models.ImageField(blank=True, default=None, null=True, upload_to='static/plants/main_images/')),
            ],
        ),
        migrations.CreateModel(
            name='PlantImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('img', models.ImageField(upload_to='static/plants/images/')),
                ('plant', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plants.plant')),
            ],
        ),
    ]
