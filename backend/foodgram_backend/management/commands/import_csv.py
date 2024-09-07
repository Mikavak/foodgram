from django.core.management.base import BaseCommand
import pandas as pd

from api.models import Ingredient


class Command(BaseCommand):
    help = 'Import data from a CSV file'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str)

    def handle(self, *args, **kwargs):
        csv_file = kwargs['csv_file']
        df = pd.read_csv(csv_file)
        for _, row in df.iterrows():
            Ingredient.objects.create(
                name=row['name'],
                measurement_unit=row['measurement_unit']
            )
        self.stdout.write(self.style.SUCCESS('Successfully imported data'))
