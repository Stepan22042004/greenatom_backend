import csv

from waste.settings import BASE_DIR
from django.core.management import BaseCommand
from organisations.models import Capacity

BASE_DIR = str(BASE_DIR.parents[0]) + r'\data'


class Command(BaseCommand):

    def handle(self, *args, **kwargs):
        self.import_ingredients()

    def import_ingredients(self):
        with open(
            BASE_DIR + r'\materials.csv',
            'r',
            encoding='utf-8'
        ) as file:
            reader = csv.reader(file)
            next(reader)
            for row in reader:
                Capacity.objects.get_or_create(
                    material=row[0]
                )
