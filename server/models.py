from django.contrib.gis.db import models

class EGridPlant(models.Model):
  pid = models.IntegerField('Plant ID EGrid 2020', primary_key=True)
  pname = models.CharField('Plant Name', max_length=128)
  location = models.PointField()

  def __str__(self):
    return f'{self.id}: {self.pname}'
  
