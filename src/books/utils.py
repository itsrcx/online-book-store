import csv
from .models import Book  
def import_data_from_csv(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as csv_file:
            csv_reader = csv.DictReader(csv_file)
            for row in csv_reader:
                title = row['title']
                author = row['author']
                genre = row['genre']
                price = float(row['price'])
                quantity = int(row['quantity'])
                description = row['description']

                # Create a new instance of your model
                book = Book(
                    title=title,
                    author=author,
                    genre=genre,
                    price=price,
                    quantity=quantity,
                    description=description
                )
                book.save()  # Save the model instance to the database

        return True, "Data imported successfully."

    except Exception as e:
        return False, str(e)