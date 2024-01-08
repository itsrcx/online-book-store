import csv
from django.core.management.base import BaseCommand
from books.models import Book, Genre
from django.utils.text import slugify   

class Command(BaseCommand):
    help = 'Import data from a CSV file into the Book model'

    def add_arguments(self, parser):
        parser.add_argument('csv_file', type=str, help='Path to the CSV file to import')

    def handle(self, *args, **options):
        csv_file_path = options['csv_file']
        unique_genres = set()  # To store unique genre names

        # Step 1: Process the CSV file to add unique genres to the Genre model
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                genre_name = row['genre']

                # Check if the genre is unique
                if genre_name not in unique_genres:
                    unique_genres.add(genre_name)  # Add to set of unique genres

                    # Create or retrieve the Genre object with a unique slug
                    genre, created = Genre.objects.get_or_create(
                        name=genre_name,
                        slug=slugify(genre_name)  # Use slugify to generate a unique slug
                    )

                    if created:
                        self.stdout.write(self.style.SUCCESS(f'Created Genre: {genre_name}'))
                    else:
                        self.stdout.write(self.style.SUCCESS(f'Retrieved Genre: {genre_name}'))

        # Step 2: Process the CSV file again to add books with their respective genres
        with open(csv_file_path, 'r', newline='', encoding='utf-8') as csv_file:
            reader = csv.DictReader(csv_file)
            for row in reader:
                genre_name = row['genre']

                # Retrieve the Genre object using filter instead of get
                genres = Genre.objects.filter(name=genre_name)

                # Choose the first genre object if exists, or handle the situation where multiple objects are returned
                if genres.exists():
                    genre = genres.first()
                else:
                    # Handle the case where no genre is found
                    self.stdout.write(self.style.ERROR(f'No Genre found for: {genre_name}'))
                    continue

                # Create a Book object with the associated genre
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