from csv import DictReader
from django.core.management.base import BaseCommand
from reviews.models import Title


class Command(BaseCommand):
    help = 'Импортирует данные в модель Titles_genre'

    def handle(self, *args, **options):

        # if Titles.objects.exists():
        #     print('title_genre data already loaded..exiting.')
        #     return

        print('Loading category data')

        for row in DictReader(open('static/data/genre_title.csv')):
            title = Title.objects.get(id=row['titles_id'])
            title.genre.add(row['genres_id'])
            title.save()
