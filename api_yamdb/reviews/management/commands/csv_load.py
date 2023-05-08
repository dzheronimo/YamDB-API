from csv import DictReader

from django.conf import settings
from django.core.management.base import BaseCommand

from reviews.models import Category, Comment, Genre, Review, Title, User

FILE_HANDLE = (
    (User, 'users.csv'),
    (Category, 'category.csv'),
    (Genre, 'genre.csv'),
    (Title, 'titles.csv'),
    (Title.genre.through, 'genre_title.csv'),
    (Review, 'review.csv'),
    (Comment, 'comments.csv'),
)


def replace_field(model, table):
    fields_list = model._meta.fields
    fields = {field.name: field.attname for field in fields_list}
    for row in table:
        for field in list(row):
            if field in fields and field != fields[field.replace('_id', '')]:
                row[fields[field]] = row.pop(field)


class Command(BaseCommand):
    def handle(self, *args, **options):
        for model, file_name in FILE_HANDLE:
            path = f'{settings.BASE_DIR}/static/data/{file_name}'
            try:
                with open(path, mode='r', encoding="utf-8") as csv_file:
                    reader = DictReader(csv_file)
                    table = list(reader)
                    replace_field(model, table)
                    model.objects.bulk_create(model(**row) for row in table)
                self.stdout.write(self.style.SUCCESS(f'{file_name} загружен'))
            except OSError as error:
                self.stderr.write(f'Проблема с файлом {error}')
            except Exception as error:
                self.stderr.write(f'Ошибка {error}')
