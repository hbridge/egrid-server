from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.measure import Distance

class EGridPlant(models.Model):
  pid = models.IntegerField('Plant ID EGrid 2020', primary_key=True)
  pname = models.CharField('Plant Name', max_length=128)
  location = models.PointField()

  def __str__(self):
    return f'{self.pid}: {self.pname} {self.location}'
  
  def plants_near(lat: float, lng: float, radius_miles: float):
    radius_center = Point(lng, lat)
    return EGridPlant.objects.filter(
      location__distance_lt=(radius_center, Distance(mi=radius_miles))
    )
