from csv import DictReader

from django.core.management.base import BaseCommand
from reviews.models import User


class Command(BaseCommand):
    help = 'Импортирует данные в модель User'

    def handle(self, *args, **options):

        if User.objects.exists():
            print('Users data already loaded..exiting.')
            return

        print('Loading category data')

        for row in DictReader(open('static/data/users.csv')):
            user = User(
                id=row['id'],
                username=row['username'],
                email=row['email'],
                role=row['role'],
                bio=row['bio'],
                first_name=row['first_name'],
                last_name=row['last_name']
            )
            user.save()
