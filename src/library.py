from .models import Book
from .storage import Storage

class Library:
    def __init__(self):
        self.storage = Storage()
        self.books = self.storage.load()
        self._next_id = self._calculate_next_id()

    def _calculate_next_id(self):
        if not self.books:
            return 1
        return max(book.id for book in self.books) + 1

    def add_book(self, title, author, genre, year, description):
        book = Book(
            id=self._next_id,
            title=title,
            author=author,
            genre=genre,
            year=year,
            description=description
        )
        self.books.append(book)
        self._next_id += 1
        self.storage.save(self.books)
        return book.id

    def find_by_id(self, book_id):
        for book in self.books:
            if book.id == book_id:
                return book
        return None

    def set_read(self, book_id, read_status):
        book = self.find_by_id(book_id)
        if not book:
            return 1
        if book.read == read_status:
            return 2
        book.read = read_status
        self.storage.save(self.books)
        return 0

    def set_favorite(self, book_id, favorite_status):
        book = self.find_by_id(book_id)
        if not book:
            return 1
        if book.favorite == favorite_status:
            return 2
        book.favorite = favorite_status
        self.storage.save(self.books)
        return 0

    def delete_book(self, book_id):
        book = self.find_by_id(book_id)
        if book:
            self.books.remove(book)
            self.storage.save(self.books)
            return True
        return False

    def search(self, keyword):
        keyword = keyword.lower()
        results = []
        for book in self.books:
            if (keyword in book.title.lower() or
                keyword in book.author.lower() or
                keyword in book.description.lower()):
                results.append(book)
        return results

    def list_books(self, sort_by=None, filter_genre=None, filter_read=None):
        books = self.books[:]
        if filter_genre:
            books = [b for b in books if b.genre.lower() == filter_genre.lower()]
        if filter_read is not None:
            books = [b for b in books if b.read == filter_read]
        if sort_by == 'title':
            books.sort(key=lambda x: x.title.lower())
        elif sort_by == 'author':
            books.sort(key=lambda x: x.author.lower())
        elif sort_by == 'year':
            books.sort(key=lambda x: x.year)
        return books

    def get_favorites(self):
        return [b for b in self.books if b.favorite]
