import csv
from django.core.management.base import BaseCommand
from books.models import Book  

class Command(BaseCommand):
    help = 'Import data from a CSV file into the Book model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to import')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                book = Book(
                    title=row['title'],
                    author=row['author'],
                    genre=row['genre'],
                    price=float(row['price']),
                    quantity=int(row['quantity']),
                    description=row['description']
                )
                book.save() 

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))

