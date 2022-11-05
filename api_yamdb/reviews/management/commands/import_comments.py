from csv import DictReader
from django.core.management.base import BaseCommand
from reviews.models import Comments


class Command(BaseCommand):
    help = 'Импортирует данные в модель Comments'

    def handle(self, *args, **options):

        if Comments.objects.exists():
            print('Comments data already loaded..exiting.')
            return

        print('Loading category data')

        for row in DictReader(open('static/data/comments.csv')):
            comments = Comments(
                review_id=row['review_id'],
                text=row['text'],
                author_id=row['author'],
                pub_date=row['pub_date'],
            )
            comments.save()
