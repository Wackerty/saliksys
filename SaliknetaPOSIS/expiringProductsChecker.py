import os

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "SaliknetaPOSIS.settings")
import django
django.setup()

from salikneta.models import *
from datetime import date

products = ProductBatch.objects.all()
expiringProducts = []
today = date.today()

for product in products:
    expiringDate = product.expiringDate
    print(today - expiringDate)