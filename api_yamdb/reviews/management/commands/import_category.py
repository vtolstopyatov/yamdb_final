from csv import DictReader
from django.core.management.base import BaseCommand
from reviews.models import Categories


class Command(BaseCommand):
    help = 'Импортирует данные в модель Categories'

    def handle(self, *args, **options):

        if Categories.objects.exists():
            print('category data already loaded..exiting.')
            return

        print('Loading category data')

        for row in DictReader(open('static/data/category.csv')):
            cat = Categories(
                name=row['name'],
                slug=row['slug']
            )
            cat.save()
