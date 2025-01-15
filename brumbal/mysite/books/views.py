from django.db.models import F
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse
from django.template import loader
from django.http import Http404
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.views import generic
from .models import Book, Review
from django.utils import timezone
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm


class IndexView(generic.ListView):
    template_name = "books/index.html"
    context_object_name = "latest_book_list"

    def get_queryset(self):
        return Book.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:12]


class DetailView(generic.DetailView):
    model = Book
    template_name = "books/detail.html"

    def get_queryset(self):
        return Book.objects.filter(pub_date__lte=timezone.now())


class ResultsView(generic.DetailView):
    model = Book
    template_name = "books/results.html"


def rating(request, book_id):
    book = get_object_or_404(Book, pk=book_id)
    try:
        selected_review = book.review_set.get(pk=request.POST["review"])
    except (KeyError, Review.DoesNotExist):
        return render(request, "books/detail.html", {
            "book": book,
            "error_message": "You didn't select a review.",
        })
    else:
        selected_review.rating = F("rating") + 1
        selected_review.save()
        selected_review.refresh_from_db()
        redirect_url = reverse("books:results", args=(book.id,))
        print("Redirecting to:", redirect_url)
        return render(request, "books/results.html", {"book": book})

def register_view(request):
    if request.method == "POST":
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("books")
    else:
        form = UserCreationForm()
    return render(request, "books/register.html", { "form": form})

def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            return redirect()
    else:
        form = AuthenticationForm()
    return render(request, "books/login.html", {"form": form})