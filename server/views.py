from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import EGridPlant
from .serializers import EGridPlantSerializer

def homePageView(request):
  return HttpResponse("Hello world!")


DEFAULT_DISTANCE = 10

class EGridPlantViewSet(viewsets.ReadOnlyModelViewSet):

  queryset = EGridPlant.objects.all().order_by('pid')
  serializer_class = EGridPlantSerializer

  def get_queryset(self):
    lat = self.request.query_params.get('lat')
    lng = self.request.query_params.get('lng')
    if lat == None or lng == None:
      return EGridPlant.objects.all().order_by('pid')

    dist = self.request.query_params.get('dist') or DEFAULT_DISTANCE

    return EGridPlant.plants_near(float(lat), float(lng), dist)