from django.shortcuts import render
from django.http import HttpResponse
from rest_framework import viewsets
from .models import EGridPlant
from .serializers import EGridPlantSerializer

def homePageView(request):
  return HttpResponse("Hello world!")


class EGridPlantViewSet(viewsets.ModelViewSet):
  queryset = EGridPlant.objects.all().order_by('pid')
  serializer_class = EGridPlantSerializer
  