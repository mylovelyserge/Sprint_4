import pytest
from main import BooksCollector


class TestBooksCollector:

    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize('name, should_add', [
        ('A', True),
        ('A' * 40, True),
        ('A' * 41, False),
        ('', False),
    ])
    def test_add_new_book_length_boundary(self, name, should_add):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert (name in collector.get_books_genre()) == should_add

    def test_add_new_book_no_duplicate(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.add_new_book('Дюна')
        assert len(collector.get_books_genre()) == 1

    def test_set_book_genre_valid(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')
        assert collector.get_book_genre('Дюна') == 'Фантастика'

    def test_set_book_genre_unknown_genre_not_set(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Биография')
        assert collector.get_book_genre('Дюна') == ''

    def test_get_book_genre(self):
        collector = BooksCollector()
        collector.add_new_book('1984')
        collector.set_book_genre('1984', 'Фантастика')
        assert collector.get_book_genre('1984') == 'Фантастика'

    def test_get_books_with_specific_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')
        collector.add_new_book('Оно')
        collector.set_book_genre('Оно', 'Ужасы')
        assert collector.get_books_with_specific_genre('Фантастика') == ['Дюна']

    def test_get_books_genre_returns_full_dict(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.set_book_genre('Дюна', 'Фантастика')
        assert collector.get_books_genre() == {'Дюна': 'Фантастика'}

    @pytest.mark.parametrize('genre, expected_in_result', [
        ('Фантастика', True),
        ('Мультфильмы', True),
        ('Комедии', True),
        ('Ужасы', False),
        ('Детективы', False),
    ])
    def test_get_books_for_children(self, genre, expected_in_result):
        collector = BooksCollector()
        book = 'Тестовая книга'
        collector.add_new_book(book)
        collector.set_book_genre(book, genre)
        assert (book in collector.get_books_for_children()) == expected_in_result

    def test_add_book_in_favorites_no_duplicate(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites('Дюна')
        collector.add_book_in_favorites('Дюна')
        assert collector.get_list_of_favorites_books().count('Дюна') == 1

    def test_add_book_in_favorites_not_in_books_genre(self):
        collector = BooksCollector()
        collector.add_book_in_favorites('Несуществующая книга')
        assert 'Несуществующая книга' not in collector.get_list_of_favorites_books()

    def test_delete_book_from_favorites(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.add_book_in_favorites('Дюна')
        collector.delete_book_from_favorites('Дюна')
        assert 'Дюна' not in collector.get_list_of_favorites_books()

    def test_get_list_of_favorites_books(self):
        collector = BooksCollector()
        collector.add_new_book('Дюна')
        collector.add_new_book('1984')
        collector.add_book_in_favorites('Дюна')
        collector.add_book_in_favorites('1984')
        assert collector.get_list_of_favorites_books() == ['Дюна', '1984']
