import datetime
from django.test import TestCase
from django.utils import timezone
from django.urls import reverse
from .models import Book

# Helper function to create books for testing
def create_book(book_title, days):
    """
    Create a book with the given `book_title` and published the
    given number of `days` offset to now (negative for books published
    in the past, positive for books that have yet to be published).
    """
    time = timezone.now() + datetime.timedelta(days=days)
    return Book.objects.create(title=book_title, pub_date=time)


class BookIndexViewTests(TestCase):
    def test_no_books(self):
        """
        If no books exist, an appropriate message is displayed.
        """
        response = self.client.get(reverse("books:index"))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "No books are available.")
        self.assertQuerySetEqual(response.context["latest_book_list"], [])

    def test_past_book(self):
        """
        Books with a pub_date in the past are displayed on the index page.
        """
        book = create_book(book_title="Past book.", days=-30)
        response = self.client.get(reverse("books:index"))
        self.assertQuerySetEqual(
            response.context["latest_book_list"],
            [book],
        )
        past_book = create_book(book_title="Past Book.", days=-5)
        url = reverse("books:detail", args=(past_book.id,))
        response = self.client.get(url)
        self.assertContains(response, past_book.book_title)

    def test_future_book(self):
        """
        Books with a pub_date in the future aren't displayed on the index page.
        """
        create_book(book_title="Future book.", days=30)
        response = self.client.get(reverse("books:index"))
        self.assertContains(response, "No books are available.")
        self.assertQuerySetEqual(response.context["latest_book_list"], [])
        future_book = create_book(book_title="Future book.", days=5)
        url = reverse("books:detail", args=(future_book.id,))
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_future_book_and_past_book(self):
        """
        Even if both past and future books exist, only past books are displayed.
        """
        book = create_book(book_title="Past book.", days=-30)
        create_book(book_title="Future book.", days=30)
        response = self.client.get(reverse("books:index"))
        self.assertQuerySetEqual(
            response.context["latest_book_list"],
            [book],
        )

    def test_two_past_books(self):
        """
        The books index page may display multiple books.
        """
        book1 = create_book(book_title="Past book 1.", days=-30)
        book2 = create_book(book_title="Past book 2.", days=-5)
        response = self.client.get(reverse("books:index"))
        self.assertQuerySetEqual(
            response.context["latest_book_list"],
            [book2, book1],
        )
