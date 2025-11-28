from django.urls import reverse
from django.contrib.auth import get_user_model

from rest_framework import status
from rest_framework.test import APITestCase

from .models import Book


User = get_user_model()


class BookAPITests(APITestCase):
    """
    Test suite for the Book API endpoints.

    We test:
    - CRUD operations (list, detail, create, update, delete)
    - Filtering, searching, and ordering
    - Permissions and authentication
    """

    def setUp(self):
        """
        Runs before each test.

        We create:
        - one test user
        - three Book instances
        """
        # Test user for authenticated operations
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword123",
        )

        # Some books to test with
        self.book1 = Book.objects.create(
            title="Django for Beginners",
            author="William Vincent",
            publication_year=2018,
        )
        self.book2 = Book.objects.create(
            title="Two Scoops of Django",
            author="Daniel Greenfeld",
            publication_year=2020,
        )
        self.book3 = Book.objects.create(
            title="Python Crash Course",
            author="Eric Matthes",
            publication_year=2015,
        )

    # ---------- CRUD: List & Detail ----------

    def test_list_books_returns_all_books(self):
        """
        Unauthenticated users should be able to list all books.
        """
        url = reverse("book-list")
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        # We expect 3 books created in setUp
        self.assertEqual(len(response.data), 3)

    def test_retrieve_single_book(self):
        """
        Unauthenticated users should be able to retrieve a single book.
        """
        url = reverse("book-detail", kwargs={"pk": self.book1.pk})
        response = self.client.get(url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.book1.title)
        self.assertEqual(response.data["author"], self.book1.author)

    # ---------- CRUD: Create ----------

    def test_create_book_requires_authentication(self):
        """
        Unauthenticated users should NOT be able to create a book.
        """
        url = reverse("book-create")
        data = {
            "title": "New Book",
            "author": "Unknown Author",
            "publication_year": 2024,
        }
        response = self.client.post(url, data, format="json")

        # With IsAuthenticated, anonymous users get 401 or 403 depending on settings
        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_authenticated_user_can_create_book(self):
        """
        Authenticated users should be able to create a book.
        """
        # Login using Django's test client
        self.client.login(username="testuser", password="testpassword123")

        url = reverse("book-create")
        data = {
            "title": "Brand New Book",
            "author": "Test User",
            "publication_year": 2025,
        }
        response = self.client.post(url, data, format="json")

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Book.objects.count(), 4)
        self.assertEqual(Book.objects.latest("id").title, "Brand New Book")

    # ---------- CRUD: Update ----------

    def test_update_book_requires_authentication(self):
        """
        Unauthenticated users should NOT be able to update a book.
        """
        url = reverse("book-update", kwargs={"pk": self.book1.pk})
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data, format="json")

        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )

    def test_authenticated_user_can_update_book(self):
        """
        Authenticated users should be able to update a book.
        """
        self.client.login(username="testuser", password="testpassword123")

        url = reverse("book-update", kwargs={"pk": self.book1.pk})
        data = {"title": "Django for Real Beginners"}
        response = self.client.patch(url, data, format="json")

        # Refresh from DB to get latest values
        self.book1.refresh_from_db()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.book1.title, "Django for Real Beginners")

    # ---------- CRUD: Delete ----------

    def test_delete_book_requires_authentication(self):
        """
        Unauthenticated users should NOT be able to delete a book.
        """
        url = reverse("book-delete", kwargs={"pk": self.book1.pk})
        response = self.client.delete(url)

        self.assertIn(
            response.status_code,
            [status.HTTP_401_UNAUTHORIZED, status.HTTP_403_FORBIDDEN],
        )
        # Book should still exist
        self.assertEqual(Book.objects.count(), 3)

    def test_authenticated_user_can_delete_book(self):
        """
        Authenticated users should be able to delete a book.
        """
        self.client.login(username="testuser", password="testpassword123")

        url = reverse("book-delete", kwargs={"pk": self.book1.pk})
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Book.objects.count(), 2)

    # ---------- Filtering ----------

    def test_filter_books_by_title(self):
        """
        Filter books by exact title using ?title=.
        """
        url = reverse("book-list")
        response = self.client.get(url, {"title": "Django for Beginners"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Django for Beginners")

    def test_filter_books_by_publication_year(self):
        """
        Filter books by publication_year using ?publication_year=.
        """
        url = reverse("book-list")
        response = self.client.get(url, {"publication_year": 2020})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Two Scoops of Django")

    # ---------- Searching ----------

    def test_search_books_by_title(self):
        """
        Search books by title using ?search=.
        """
        url = reverse("book-list")
        response = self.client.get(url, {"search": "Django"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertIn("Django for Beginners", titles)
        self.assertIn("Two Scoops of Django", titles)

    def test_search_books_by_author(self):
        """
        Search books by author using ?search=.
        """
        url = reverse("book-list")
        response = self.client.get(url, {"search": "Eric"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["author"], "Eric Matthes")

    # ---------- Ordering ----------

    def test_order_books_by_title_ascending(self):
        """
        Order books by title using ?ordering=title.
        """
        url = reverse("book-list")
        response = self.client.get(url, {"ordering": "title"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        titles = [book["title"] for book in response.data]
        self.assertEqual(titles, sorted(titles))

    def test_order_books_by_publication_year_descending(self):
        """
        Order books by publication_year descending using ?ordering=-publication_year.
        """
        url = reverse("book-list")
        response = self.client.get(url, {"ordering": "-publication_year"})

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        years = [book["publication_year"] for book in response.data]
        self.assertEqual(years, sorted(years, reverse=True))
