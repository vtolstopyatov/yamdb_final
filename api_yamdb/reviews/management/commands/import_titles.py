from csv import DictReader

from django.core.management.base import BaseCommand
from reviews.models import Title


class Command(BaseCommand):
    help = 'Импортирует данные в модель Titles'

    def handle(self, *args, **options):

        if Title.objects.exists():
            print('Titles data already loaded..exiting.')
            return

        print('Loading category data')

        for row in DictReader(open('static/data/titles.csv')):
            titles = Title(
                name=row['name'],
                year=row['year'],
                category_id=row['category_id']
            )
            titles.save()
