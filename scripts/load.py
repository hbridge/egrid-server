import csv
import re
from django.contrib.gis.geos import Point
from server.models import EGridPlant
from decimal import *

FILE_PATH="egrid_data/us_egrid_2020_PLNT20.csv"

def run(apps = None, schema_editor = None):
  # if not run from a migration apps and schema_editor will be none
  print(f"Importing EGrid plants from {FILE_PATH}")
  fhand = open(FILE_PATH)
  reader = csv.reader(fhand)
  next(reader) # the file contains descriptions of each column
  csv_field_names = [s.lower() for s in next(reader)] # line two contains the header
  model_to_csv_col = {}
  #map all model fields to columns in the CSV
  for field in EGridPlant._meta.get_fields():
    if field.attname == "pid" or field.attname == "location":
      continue # these are special cased for the two special cased mapping
    model_to_csv_col[field] = csv_field_names.index(field.attname)

  LAT_COL = csv_field_names.index('lat')
  LON_COL = csv_field_names.index('lon')
  PNAME_COL = csv_field_names.index('pname')

  for row in reader:
    try:
      pid = row[0]
      latitude = float(row[LAT_COL])
      longitude = float(row[LON_COL])
      pname = row[PNAME_COL]
      plant = EGridPlant(pid=pid, pname=pname, location=Point(longitude, latitude))
      for field in model_to_csv_col:
        col = model_to_csv_col[field]
        val = row[col]
        match field.get_internal_type():
          case "BooleanField":
            val = True if val == "Yes" else False
          case "DecimalField":
            val = Decimal(val) if val != "" else None
          case "FloatField":
            val = float(clean_num_str(val)) if val != "" else None
          case "IntegerField" | "PositiveSmallIntegerField":
            val = int(clean_num_str(val)) if val != "" else None
        setattr(plant, field.attname, val)
    
      plant.save()
    except Exception as e:
      print(f'Could not import {pid}: {e}')
    
  print("All rows processed")

def clean_num_str(num_str):
  return re.sub(r'[,)]',"",num_str).replace("(", "-", 1)