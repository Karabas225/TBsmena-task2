from rich.table import Table
from rich.panel import Panel
from rich import box
from .utils import console

def show_menu():
    menu_text = """
[bold cyan]1.[/bold cyan] Добавить книгу
[bold cyan]2.[/bold cyan] Показать все книги (с сортировкой/фильтрацией)
[bold cyan]3.[/bold cyan] Изменить статус прочтения
[bold cyan]4.[/bold cyan] Добавить/удалить из избранного
[bold cyan]5.[/bold cyan] Показать избранные книги
[bold cyan]6.[/bold cyan] Удалить книгу
[bold cyan]7.[/bold cyan] Поиск книг
[bold cyan]8.[/bold cyan] Статистика
[bold cyan]9.[/bold cyan] Импорт книг из другой библиотеки
[bold cyan]10.[/bold cyan] Корректировка книги по ID
[bold cyan]0.[/bold cyan] Выход
"""
    console.print(Panel(menu_text, title=" T-Библиотека ", subtitle="Ваша личная коллекция", box=box.DOUBLE_EDGE))

def get_choice():
    return input("Выберите действие: ").strip()

def input_book_details():
    title = input("Название: ").strip()
    author = input("Автор: ").strip()
    genre = input("Жанр: ").strip()
    while True:
        try:
            year = int(input("Год издания: ").strip())
            break
        except ValueError:
            console.print("[red]Год должен быть числом.[/red]")
    description = input("Краткое описание: ").strip()
    return title, author, genre, year, description

def display_books(books):
    if not books:
        console.print("[yellow]Нет книг для отображения.[/yellow]")
        return

    console.print(f"[bold green]Найдено книг: {len(books)}[/bold green]")
    table = Table(show_header=True, header_style="bold magenta", box=box.MINIMAL_HEAVY_HEAD)
    table.add_column("ID", style="dim", width=6)
    table.add_column("Название", width=30)
    table.add_column("Автор", width=20)
    table.add_column("Жанр", width=15)
    table.add_column("Год", justify="right", width=6)
    table.add_column("Статус", width=12)
    table.add_column("Изб.", width=4)

    for book in books:
        read_status = "[green][X][/green] Прочитана" if book.read else "[red][ ][/red] Не прочитана"
        fav = "*" if book.favorite else ""
        table.add_row(
            str(book.id),
            book.title[:28] + "..." if len(book.title) > 28 else book.title,
            book.author[:18] + "..." if len(book.author) > 18 else book.author,
            book.genre[:13] + "..." if len(book.genre) > 13 else book.genre,
            str(book.year),
            read_status,
            fav
        )
    console.print(table)

def display_message(message, style="green"):
    styles = {
        "green": "bold green",
        "red": "bold red",
        "yellow": "bold yellow",
        "cyan": "bold cyan",
        "blue": "bold blue"
    }
    console.print(f"[{styles.get(style, style)}]{message}[/{styles.get(style, style)}]")
