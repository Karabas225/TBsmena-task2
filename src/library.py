import json
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

    def update_book(self, book_id, **kwargs):
        """Обновляет поля книги. Возвращает True при успехе."""
        book = self.find_by_id(book_id)
        if not book:
            return False
        allowed = {'title', 'author', 'genre', 'year', 'description'}
        for key, value in kwargs.items():
            if key in allowed:
                setattr(book, key, value)
        self.storage.save(self.books)
        return True

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

    def get_statistics(self):
        total = len(self.books)
        read = sum(1 for b in self.books if b.read)
        unread = total - read
        favorites = sum(1 for b in self.books if b.favorite)

        # Подсчёт избранных книг по жанрам
        genre_counter = {}
        for b in self.books:
            if b.favorite:
                genre = b.genre.strip()
                if genre:
                    genre_counter[genre] = genre_counter.get(genre, 0) + 1

        # Определение любимого жанра (с максимальным числом избранных)
        favorite_genre = None
        if genre_counter:
            max_count = max(genre_counter.values())
            # Выбираем первый по алфавиту среди жанров с максимумом
            favorite_genre = min(
                (g for g, cnt in genre_counter.items() if cnt == max_count),
                key=lambda x: x.lower()
            )

        return {
            'total': total,
            'read': read,
            'unread': unread,
            'favorites': favorites,
            'favorite_genre': favorite_genre,
            'genre_counter': genre_counter
        }

    def import_books(self, filepath):
        """
        Импортирует книги из JSON-файла.
        Возвращает кортеж (количество добавленных, количество пропущенных).
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
        except Exception as e:
            raise Exception(f"Ошибка чтения файла: {e}")

        added = 0
        skipped = 0

        existing_keys = {(b.title.lower(), b.author.lower()) for b in self.books}

        for item in data:
            try:
                title = item.get('title', '').strip()
                author = item.get('author', '').strip()
                if not title or not author:
                    skipped += 1
                    continue

                key = (title.lower(), author.lower())
                if key in existing_keys:
                    skipped += 1
                    continue

                # Создаём новую книгу, сбрасывая статусы
                book = Book(
                    id=self._next_id,
                    title=title,
                    author=author,
                    genre=item.get('genre', '').strip(),
                    year=int(item.get('year', 0)) if str(item.get('year', '')).isdigit() else 0,
                    description=item.get('description', '').strip(),
                    read=False,
                    favorite=False
                )
                self.books.append(book)
                self._next_id += 1
                existing_keys.add(key)
                added += 1

            except Exception:
                skipped += 1

        if added > 0:
            self.storage.save(self.books)

        return added, skipped
