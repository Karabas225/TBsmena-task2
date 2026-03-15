import sys
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

        elif choice == '0':
            ui.display_message("До свидания!", style="cyan")
            sys.exit(0)

        else:
            ui.display_message("Неверный пункт меню.", style="red")
            input("Нажмите Enter...")

if __name__ == "__main__":
    main()  