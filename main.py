import sys
import os
from rich.panel import Panel
from src.library import Library
from src import ui
from src.utils import clear_screen, console

def main():
    lib = Library()
    clear_screen()
    console.print(Panel.fit("[bold cyan]Добро пожаловать в T-Библиотеку![/bold cyan]", border_style="blue"))
    input("Нажмите Enter, чтобы продолжить...")

    while True:
        clear_screen()
        ui.show_menu()
        choice = ui.get_choice()

        if choice == '1':
            try:
                title, author, genre, year, description = ui.input_book_details()
                book_id = lib.add_book(title, author, genre, year, description)
                ui.display_message(f"Книга добавлена с ID {book_id}.", style="green")
            except Exception as e:
                ui.display_message(f"Ошибка: {e}", style="red")
            input("Нажмите Enter...")

        elif choice == '2':
            filter_genre = input("Фильтр по жанру (Enter - без фильтра): ").strip() or None
            filter_read_choice = input("Фильтр по статусу (1 - прочитанные, 2 - непрочитанные, Enter - все): ").strip()
            filter_read = None
            if filter_read_choice == '1':
                filter_read = True
            elif filter_read_choice == '2':
                filter_read = False

            console.print("[bold cyan]Сортировка:[/bold cyan]")
            console.print("  1 - по названию")
            console.print("  2 - по автору")
            console.print("  3 - по году")
            console.print("  Enter - без сортировки")
            sort_choice = input("Выберите вариант: ").strip()
            sort_map = {'1': 'title', '2': 'author', '3': 'year'}
            sort_by = sort_map.get(sort_choice)

            books = lib.list_books(sort_by=sort_by, filter_genre=filter_genre, filter_read=filter_read)
            ui.display_books(books)
            input("Нажмите Enter...")

        elif choice == '3':
            try:
                book_id = int(input("Введите ID книги: ").strip())
            except ValueError:
                ui.display_message("ID должен быть числом.", style="red")
                input("Нажмите Enter...")
                continue

            console.print("Статус: 1 - прочитана, 2 - не прочитана")
            read_choice = input("Выберите: ").strip()
            if read_choice == '1':
                result = lib.set_read(book_id, True)
                if result == 0:
                    ui.display_message("Статус изменён на 'прочитана'.", style="green")
                elif result == 1:
                    ui.display_message(f"Книга с ID {book_id} не найдена.", style="red")
                elif result == 2:
                    ui.display_message("Книга уже прочитана.", style="yellow")
            elif read_choice == '2':
                result = lib.set_read(book_id, False)
                if result == 0:
                    ui.display_message("Статус изменён на 'не прочитана'.", style="green")
                elif result == 1:
                    ui.display_message(f"Книга с ID {book_id} не найдена.", style="red")
                elif result == 2:
                    ui.display_message("Книга уже не прочитана.", style="yellow")
            else:
                ui.display_message("Неверный выбор.", style="red")
            input("Нажмите Enter...")

        elif choice == '4':
            try:
                book_id = int(input("Введите ID книги: ").strip())
            except ValueError:
                ui.display_message("ID должен быть числом.", style="red")
                input("Нажмите Enter...")
                continue

            console.print("Действие: 1 - добавить в избранное, 2 - удалить из избранного")
            fav_choice = input("Выберите: ").strip()
            if fav_choice == '1':
                result = lib.set_favorite(book_id, True)
                if result == 0:
                    ui.display_message("Книга добавлена в избранное (*).", style="green")
                elif result == 1:
                    ui.display_message(f"Книга с ID {book_id} не найдена.", style="red")
                elif result == 2:
                    ui.display_message("Книга уже в избранном.", style="yellow")
            elif fav_choice == '2':
                result = lib.set_favorite(book_id, False)
                if result == 0:
                    ui.display_message("Книга удалена из избранного.", style="green")
                elif result == 1:
                    ui.display_message(f"Книга с ID {book_id} не найдена.", style="red")
                elif result == 2:
                    ui.display_message("Книга не была в избранном.", style="yellow")
            else:
                ui.display_message("Неверный выбор.", style="red")
            input("Нажмите Enter...")

        elif choice == '5':
            favorites = lib.get_favorites()
            ui.display_books(favorites)
            input("Нажмите Enter...")

        elif choice == '6':
            try:
                book_id = int(input("Введите ID книги для удаления: ").strip())
            except ValueError:
                ui.display_message("ID должен быть числом.", style="red")
                input("Нажмите Enter...")
                continue
            if lib.delete_book(book_id):
                ui.display_message("Книга удалена.", style="green")
            else:
                ui.display_message(f"Книга с ID {book_id} не найдена.", style="red")
            input("Нажмите Enter...")

        elif choice == '7':
            keyword = input("Введите ключевое слово для поиска: ").strip()
            results = lib.search(keyword)
            ui.display_books(results)
            input("Нажмите Enter...")

        elif choice == '8':
            clear_screen()
            stats = lib.get_statistics()
            console.print("[bold cyan]Статистика библиотеки[/bold cyan]")
            if stats['total'] == 0:
                console.print("[yellow]Библиотека пуста.[/yellow]")
            else:
                console.print(f"Всего книг: {stats['total']}")
                console.print(f"Прочитано: {stats['read']} ({stats['read']/stats['total']*100:.1f}%)")
                console.print(f"Не прочитано: {stats['unread']}")
                console.print(f"В избранном: {stats['favorites']}")
                if stats['favorite_genre']:
                    console.print(f"Любимый жанр (по избранным): {stats['favorite_genre']}")
                else:
                    console.print("Любимый жанр: пока нет избранных книг.")
            input("Нажмите Enter...")

        elif choice == '9':
            clear_screen()
            console.print("[bold]Импорт книг из другой библиотеки[/bold]")
            filepath = input("Введите полный или относительный путь к JSON-файлу: ").strip()
            if not filepath:
                ui.display_message("Импорт отменён.", "yellow")
                input("Нажмите Enter...")
                continue

            try:
                added, skipped = lib.import_books(filepath)
                ui.display_message(f"Импорт завершён. Добавлено: {added}, пропущено дубликатов/ошибок: {skipped}", "green")
            except Exception as e:
                ui.display_message(f"Ошибка импорта: {e}", "red")
            input("Нажмите Enter...")

        elif choice == '10':
            try:
                book_id = int(input("Введите ID книги для корректировки: ").strip())
            except ValueError:
                ui.display_message("ID должен быть числом.", style="red")
                input("Нажмите Enter...")
                continue

            book = lib.find_by_id(book_id)
            if not book:
                ui.display_message(f"Книга с ID {book_id} не найдена.", style="red")
                input("Нажмите Enter...")
                continue

            console.print("[bold cyan]Текущие данные книги:[/bold cyan]")
            console.print(f"Название: {book.title}")
            console.print(f"Автор: {book.author}")
            console.print(f"Жанр: {book.genre}")
            console.print(f"Год: {book.year}")
            console.print(f"Описание: {book.description}")
            console.print(f"Статус прочтения: {'прочитана' if book.read else 'не прочитана'}")
            console.print(f"В избранном: {'да' if book.favorite else 'нет'}")
            console.print()

            new_title = input(f"Новое название [{book.title}]: ").strip()
            new_author = input(f"Новый автор [{book.author}]: ").strip()
            new_genre = input(f"Новый жанр [{book.genre}]: ").strip()
            new_year_str = input(f"Новый год [{book.year}]: ").strip()
            new_description = input(f"Новое описание [{book.description}]: ").strip()

            updates = {}
            if new_title:
                updates['title'] = new_title
            if new_author:
                updates['author'] = new_author
            if new_genre:
                updates['genre'] = new_genre
            if new_year_str:
                try:
                    updates['year'] = int(new_year_str)
                except ValueError:
                    ui.display_message("Год должен быть числом. Поле не будет изменено.", "yellow")
            if new_description:
                updates['description'] = new_description

            if not updates:
                ui.display_message("Нет изменений.", "yellow")
            else:
                success = lib.update_book(book_id, **updates)
                if success:
                    ui.display_message("Книга успешно обновлена.", "green")
                else:
                    ui.display_message("Ошибка при обновлении.", "red")
            input("Нажмите Enter...")

        elif choice == '0':
            ui.display_message("До свидания!", style="cyan")
            sys.exit(0)

        else:
            ui.display_message("Неверный пункт меню.", style="red")
            input("Нажмите Enter...")

if __name__ == "__main__":
    main()
