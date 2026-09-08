import pytest
from main import BooksCollector

class TestBooksCollector:

    # Тесты метода add_new_book

    def test_add_new_book_add_two_books(self):
        collector = BooksCollector()
        collector.add_new_book('Гордость и предубеждение и зомби')
        collector.add_new_book('Что делать, если ваш кот хочет вас убить')
        assert len(collector.get_books_genre()) == 2

    @pytest.mark.parametrize(
        'invalid_book_name',
        ['', 'G' * 41, 'A' * 42]
    )
    def test_add_new_book_invalid_name(self, invalid_book_name):
        collector = BooksCollector()
        collector.add_new_book(invalid_book_name)
        assert invalid_book_name not in collector.get_books_genre()

    def test_add_new_book_name_40_characters(self):
        collector = BooksCollector()
        book_name = 'А' * 40
        collector.add_new_book(book_name)
        assert book_name in collector.get_books_genre()

    # Тесты работы с жанрами

    def test_add_new_book_without_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Война и мир')
        assert collector.get_book_genre('Война и мир') == ''

    @pytest.mark.parametrize(
        'book_name, genre, expected_genre',
        [
            ('Книга 1', 'Фантастика', 'Фантастика'), # Валидный жанр
            ('Книга 1', 'Роман', ''),              # Невалидный жанр (остается пустым)
        ]
    )
    def test_set_book_genre(self, book_name, genre, expected_genre):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.set_book_genre(book_name, genre)
        assert collector.get_book_genre(book_name) == expected_genre

    @pytest.mark.parametrize(
        'books_genre, requested_genre, expected_result',
        [
            ({}, 'Фантастика', []),
            ({'Книга 1': 'Фантастика', 'Книга 2': 'Комедии'}, 'Фантастика', ['Книга 1']),
            ({'Книга 1': 'Комедии', 'Книга 2': 'Ужасы'}, 'Фантастика', []),
            ({'Книга 1': 'Фантастика', 'Книга 2': 'Комедии'}, 'Роман', []),
            ({'Книга 1': 'Фантастика', 'Книга 2': 'Комедии', 'Книга 3': 'Фантастика'}, 'Фантастика', ['Книга 1', 'Книга 3'])
        ]
    )
    def test_get_books_with_specific_genre(self, books_genre, requested_genre, expected_result):
        collector = BooksCollector()
        collector.books_genre = books_genre
        result = collector.get_books_with_specific_genre(requested_genre)
        assert result == expected_result

    @pytest.mark.parametrize(
        'books_genre',
        [{}, {'Война и мир': ''}, {'Книга 1': 'Фантастика', 'Книга 2': 'Комедии'}]
    )
    def test_get_books_genre(self, books_genre):
        collector = BooksCollector()
        collector.books_genre = books_genre
        assert collector.get_books_genre() == books_genre

    def test_get_books_for_children(self):
        collector = BooksCollector()
        # Добавляем книгу с "детским" жанром
        collector.add_new_book('Басни Крылова')
        collector.set_book_genre('Басни Крылова', 'Комедии')
        # Добавляем книгу с "взрослым" жанром
        collector.add_new_book('Человек-мотылёк')
        collector.set_book_genre('Человек-мотылёк', 'Ужасы')
        
        result = collector.get_books_for_children()
        assert 'Басни Крылова' in result
        assert 'Человек-мотылёк' not in result

    # Тесты Избранного

    @pytest.mark.parametrize(
        'book_name',
        ['Гарри Поттер и философский камень', 'Двенадцать стульев']
    )
    def test_add_book_in_favorites_only_once(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.add_book_in_favorites(book_name)
        assert collector.get_list_of_favorites_books() == [book_name]

    @pytest.mark.parametrize(
        'book_name',
        ['Гарри Поттер и философский камень', 'Двенадцать стульев']
    )
    def test_delete_book_from_favorites(self, book_name):
        collector = BooksCollector()
        collector.add_new_book(book_name)
        collector.add_book_in_favorites(book_name)
        collector.delete_book_from_favorites(book_name)
        assert collector.get_list_of_favorites_books() == []

    @pytest.mark.parametrize(
        'favorites_books',
        [
            [],
            ['Гарри Поттер и философский камень'],
            ['Гарри Поттер и философский камень', 'Двенадцать стульев']
        ]
    )
    def test_get_list_of_favorites_books(self, favorites_books):
        collector = BooksCollector()
        for book_name in favorites_books:
            collector.add_new_book(book_name)
            collector.add_book_in_favorites(book_name)
        assert collector.get_list_of_favorites_books() == favorites_books
