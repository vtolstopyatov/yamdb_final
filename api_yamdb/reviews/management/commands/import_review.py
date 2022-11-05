from csv import DictReader
from django.core.management.base import BaseCommand
from reviews.models import Review


class Command(BaseCommand):
    help = 'Импортирует данные в модель Review'

    def handle(self, *args, **options):

        if Review.objects.exists():
            print('Reviews data already loaded..exiting.')
            return

        print('Loading category data')

        for row in DictReader(open('static/data/review.csv')):
            review = Review(
                title_id=row['title_id'],
                text=row['text'],
                author_id=row['author'],
                score=row['score'],
                pub_date=row['pub_date'],
            )
            review.save()
