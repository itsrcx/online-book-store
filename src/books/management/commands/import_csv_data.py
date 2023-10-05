import csv
from django.core.management.base import BaseCommand
from books.models import Book, Genre

class Command(BaseCommand):
    help = 'Import data from a CSV file into the Book model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to import')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        unique_genres = set()  # To store unique genre names

        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                genre_name = row['genre']

                # Check if the genre is unique
                if genre_name not in unique_genres:
                    unique_genres.add(genre_name)  # Add to set of unique genres

                    # Create or retrieve the Genre object
                    genre, created = Genre.objects.get_or_create(name=genre_name)

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created Genre: {genre_name}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Retrieved Genre: {genre_name}'))

                    book = Book(
                        title=row['title'],
                        author=row['author'],
                        genre=genre, 
                        price=float(row['price']),
                        quantity=int(row['quantity']),
                        description=row['description']
                    )
                    book.save()

        self.stdout.write(self.style.SUCCESS('Data imported successfully'))
