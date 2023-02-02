from django.contrib.gis.db import models
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from django.contrib.gis.measure import D
from django.utils.translation import gettext_lazy as _


class EGridPlant(models.Model):
  class FuelType(models.TextChoices):
    AB = 'AB', _('Agricultural byproduct')
    BFG = 'BFG', _('Blast furnace gas')
    BIT = 'BIT', _('Bituminous coal')
    BLQ = 'BLQ', _('Black liquor')
    COG = 'COG', _('Coke oven gas')
    DFO = 'DFO', _('Distillate fuel oil, light fuel oil, diesel oil')
    GEO = 'GEO', _('Geothermal')
    H = 'H', _('Hydrogen')
    JF = 'JF', _('Jet fuel')
    KER = 'KER', _('Kerosene')
    LFG = 'LFG', _('Landfill gas')
    LIG = 'LIG', _('Lignite coal')
    MSW = 'MSW', _('Municipal solid waste ')
    MWH = 'MWH', _('Electricity used for energy storage (megawatt hour)')
    NG = 'NG', _('Natural gas')
    NUC = 'NUC', _('Nuclear')
    OBG = 'OBG', _('Other biomass gas (digester gas, methane, and other biomass gases)')
    OBL = 'OBL', _('Other biomass liquids')
    OBS = 'OBS', _('Other biomass solid')
    OG = 'OG', _('Other gas')
    OTH = 'OTH', _('Other')
    PC = 'PC', _('Petroleum coke')
    PG = 'PG', _('Gaseous propane')
    PRG = 'PRG', _('Process gas')
    PUR = 'PUR', _('Purchased steam')
    RC = 'RC', _('Refined coal')
    RFO = 'RFO', _('Residual fuel oil, heavy fuel oil, petroleum')
    SGC = 'SGC', _('Coal-derived synthetic gas')
    SLW = 'SLW', _('Sludge waste')
    SUB = 'SUB', _('Subbituminous coal')
    SUN = 'SUN', _('Solar')
    TDF = 'TDF', _('Tire-derived fuel')
    WAT = 'WAT', _('Water')
    WC = 'WC', _('Waste coal')
    WDL = 'WDL', _('Wood, wood waste liquid')
    WDS = 'WDS', _('Wood, wood waste solid')
    WH = 'WH', _('Waste heat')
    WND = 'WND', _('Wind')
    WO = 'WO', _('Waste oil')

  class FuelCategory(models.TextChoices):
    COAL = 'COAL', _('Coal')
    OIL = 'OIL', _('Oil')
    GAS = 'GAS', _('Gas')
    OFSL = 'OFSL', _('Other fossil fuel')
    NUCLEAR = 'NUCLEAR', _('Nuclear')
    HYDRO = 'HYDRO', _('Hydro')
    SOLAR = 'SOLAR', _('Solar')
    WIND = 'WIND', _('Wind')
    GEOTHERMAL = 'GEOTHERMAL', _('Geothermal')
    OTHF = 'OTHF', _('Waste heat, hydrogen, purchased or unknown')
    BIOMASS = 'BIOMASS', _('Biomass')

  pid = models.IntegerField('Plant ID EGrid 2020', primary_key=True)
  pname = models.CharField('Plant Name', max_length=128)
  lat = models.FloatField('Latitude', null=True)
  lon = models.FloatField('Longitude', null=True)
  location = models.PointField()
  pstatabb = models.CharField('Plant state abbreviation', max_length=2, blank=True)
  oprname = models.CharField('Plant transmission or distribution system owner', max_length=50, blank=True)
  utlsrvnm = models.CharField('Utility name', max_length=128, blank=True)
  numunt = models.PositiveSmallIntegerField('Number of units', null=True)
  numgen = models.PositiveSmallIntegerField('Number of generators', null=True)
  plprmfl = models.CharField('Plant primary fuel', max_length=3, choices=FuelType.choices, blank=True)
  plfuelct = models.CharField('Plant primary fuel category', max_length=10, choices=FuelCategory.choices, blank=True)
  coalflag = models.BooleanField('Flag indicating if the plant burned or generated any amount of coal', default=False)
  capfac = models.DecimalField('Plant capacity factor (annual production / nameplate)', max_digits=5, decimal_places=4, null=True)
  namepcap = models.FloatField('Plant nameplate (theoretical) capacity (MW)', null=True)
  plngenan = models.IntegerField('Plant annual net generation (MWh)', null=True)
  plngenoz = models.IntegerField('Plant annual NOx emissions (tons)', null=True)
  plnoxan = models.IntegerField('Plant ozone season NOx emissions (tons)', null=True)
  plnoxoz = models.IntegerField('Plant annual SO2 emissions (tons)', null=True)
  plso2an = models.IntegerField('Plant annual CO2 emissions (tons)', null=True)
  plco2an = models.IntegerField('Plant annual CH4 emissions (lbs)', null=True)
  plch4an = models.IntegerField('Plant annual N2O emissions (lbs)', null=True)
  pln2oan = models.IntegerField('Plant annual CO2 equivalent emissions (tons)', null=True)
  plco2eqa = models.IntegerField('Plant annual Hg emissions (lbs)', null=True)
  plhgan = models.IntegerField('Plant annual NOx total output emission rate (lb/MWh)', null=True)  

  def __str__(self):
    return f'{self.pid}: {self.pname} {self.location}'
  
  def plants_near(lat: float, lng: float, radius_miles: float):
    radius_center = Point(lng, lat)
    return (EGridPlant.objects
      .filter(location__distance_lt=(radius_center, D(mi=radius_miles)))
      .annotate(distance=Distance("location", radius_center))
      .order_by("distance")
    )
