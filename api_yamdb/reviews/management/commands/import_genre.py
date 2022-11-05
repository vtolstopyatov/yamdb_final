from csv import DictReader

from django.core.management.base import BaseCommand
from reviews.models import Genres


class Command(BaseCommand):
    help = 'Импортирует данные в модель Genres'

    def handle(self, *args, **options):

        if Genres.objects.exists():
            print('Genres data already loaded..exiting.')
            return

        print('Loading category data')

        for row in DictReader(open('static/data/genre.csv')):
            genre = Genres(
                name=row['name'],
                slug=row['slug']
            )
            genre.save()
