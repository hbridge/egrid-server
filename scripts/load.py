import csv
from django.contrib.gis.geos import Point
from server.models import EGridPlant

FILE_PATH="egrid_data/us_egrid_2020_PLNT20.csv"

def run():
  # All data in run method only will be executed 
  print(f"Importing EGrid plants from {FILE_PATH}")
  fhand = open(FILE_PATH)
  reader = csv.reader(fhand)
  next(reader)
  next(reader) # 2 header rows
  
  for row in reader:
    try:
      pid = row[0]
      pname = row[3]
      latitude = float(row[19])
      longitude = float(row[20])
      plant = EGridPlant(pid=pid, pname=pname, location=Point(longitude, latitude))
      plant.save()
    except Exception as e:
      print(f'Could not import {pid}: {e}')
    
  print("All rows processed")