import csv
from .models import Book  

def insert_books_from_csv(csv_file):
    with open(csv_file, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            # Create a Book object and save it to the database
            book = Book(
                title=row['Book Title'],
                author=row['Author Name'],
                genre=row['Genre'],
                price=row['Price (INR)'],
                quantity=row['Quantity']
            )
            book.save()

if __name__ == '__main__':
    csv_file_path = '/home/applify/book-data.csv'  # Replace with the actual path to your CSV file
    insert_books_from_csv(csv_file_path)