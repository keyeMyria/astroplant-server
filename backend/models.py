"""
Module defining backend AstroPlant models.
"""

from django.db import models
import django.contrib.auth.models
from django.contrib.auth.base_user import AbstractBaseUser
from rest_framework import serializers

class Kit(AbstractBaseUser):
    """
    Model for AstroPlant kits.

    See also:
    https://docs.djangoproject.com/en/1.9/topics/auth/customizing/#extending-the-existing-user-model
    """
    serial = models.CharField(max_length = 250, unique = True)
    type = models.CharField(max_length = 10)
    name = models.CharField(max_length = 250)
    description = models.TextField(default = "", blank = True)
    latitude = models.DecimalField(max_digits = 12, decimal_places = 4, blank = True, null = True)
    longitude = models.DecimalField(max_digits = 12, decimal_places = 4, blank = True, null = True)

    users = models.ManyToManyField(
        django.contrib.auth.models.User,
        through='KitMembership',
        through_fields=('kit', 'user'),
    )

    USERNAME_FIELD = 'serial'
    REQUIRED_FIELDS = ['type', 'name']

    def get_full_name(self):
        """
        Returns the serial of the kit.
        """
        return serial.strip()

    def get_short_name(self):
        """
        Returns the short name for the user.
        """
        return self.get_full_name()

    def __str__(self):
        return self.serial

class Experiment(models.Model):
    """
    Model for experiments.
    """
    kit = models.ForeignKey(Kit, on_delete = models.CASCADE)
    date_time_start = models.DateTimeField()
    date_time_end = models.DateTimeField(blank = True, null = True)

class KitMembership(models.Model):
    """
    Link table for kits and users, with additional data fields.
    """
    user = models.ForeignKey(django.contrib.auth.models.User, on_delete = models.CASCADE)
    kit = models.ForeignKey(Kit, on_delete = models.CASCADE)
    date_time_linked = models.DateTimeField()

    def __str__(self):
        return "%s - %s" % (self.kit, self.user)
    
class SensorType(models.Model):
    """
    Model to hold sensor types. For example, an EC sensor
    of brand A will be a row, and an EC sensor of brand B
    will be a different row.
    """

    name = models.CharField(max_length = 100)
    brand = models.CharField(max_length = 100)
    type = models.CharField(max_length = 100)
    unit = models.CharField(max_length = 100, blank = True)

    def __str__(self):
        return self.name

class Sensor(models.Model):
    """
    Model of individual sensors. Each such sensor belongs
    to a single kit.
    """

    kit = models.ForeignKey(Kit, on_delete = models.CASCADE)
    type = models.ForeignKey(SensorType, on_delete = models.CASCADE)

class Measurement(models.Model):
    """
    Model to hold sensor measurements.
    """

    sensor_type = models.ForeignKey(SensorType, on_delete = models.CASCADE)

    kit = models.ForeignKey(Kit, on_delete = models.CASCADE)

    # Null allowed, as it is possible no experiment is running
    experiment = models.ForeignKey(Experiment, on_delete = models.CASCADE, null = True)

    date_time = models.DateTimeField()
    value = models.FloatField()

class MeasurementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Measurement
        fields = ('id', 'value')
