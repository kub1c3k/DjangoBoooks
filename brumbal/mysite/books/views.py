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
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.db.models import F
from django.utils import timezone
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django import forms
from django.utils.translation import gettext_lazy as _
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views import generic
from .models import Book
from django.utils import timezone


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = "books/index.html"
    context_object_name = "latest_book_list"

    def get_queryset(self):
        return Book.objects.filter(pub_date__lte=timezone.now()).order_by("-pub_date")[:12]

class DetailView(LoginRequiredMixin, generic.DetailView):
    model = Book
    template_name = "books/detail.html"

    def get_queryset(self):
        return Book.objects.filter(pub_date__lte=timezone.now())

class ResultsView(LoginRequiredMixin, generic.DetailView):
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
        
def register(request):
    message = " "
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)  # Use CustomUserCreationForm here
        username = request.POST.get("username")
        if form.is_valid():
            user = form.save()
            login(request, user)
            message = f"Registrácia bola úspešná! Vitajte, {username}"
            return redirect("books:index")
        else:
            message = "Registrácia zlyhala. Skontrolujte chyby nižšie."
    else:
        form = CustomUserCreationForm()  # Use CustomUserCreationForm here

    return render(request, "accounts/register.html", {"form": form, "message": message})


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')  # Redirect to your desired page after login
    else:
        form = CustomAuthenticationForm()


    
    if request.user.is_authenticated:
        user = request.user
    else:
        user = None
    return render(request, "accounts/login.html", {"form": form, "user": user})
    


@login_required
def logout_view(request):
    logout(request)
    return redirect("books:login")

@login_required
def delete_user(request, pk):
    if request.user.pk != pk:
        messages.error(request, "Nie ste oprávenený zmazať tento účet.")
        return redirect('books:index')  # Redirect to a safe page
    
    user = get_object_or_404(User, pk=pk)
    
    if request.method == "POST":
        user.delete()
        messages.success(request, "Váš účet bol úspešne zmazaný.")
        return redirect('books:index')  # Redirect after successful deletion
    
    return render(request, 'accounts/confirm_delete.html', {'user': user})

from django.contrib.auth.forms import AuthenticationForm
from django import forms

class CustomAuthenticationForm(AuthenticationForm):
    username = forms.CharField(
        label='Meno',  # Custom label for username
        widget=forms.TextInput(attrs={'placeholder': 'Zadajte používateľské meno'})
    )
    password = forms.CharField(
        label='Heslo',  # Custom label for password
        widget=forms.PasswordInput(attrs={'placeholder': 'Zadajte heslo'})
    )


class CustomUserCreationForm(UserCreationForm):
    # Customizing username field
    def clean_password2(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        # Check if the passwords match
        if password1 != password2:
            raise forms.ValidationError(_('Heslá sa nezhodujú'))

        return password2

    username = forms.CharField(
        label="Používateľské meno",
        help_text="<br> musí obsahovať iba písmená, číslice a znaky @/./+/-/_.",
        error_messages={
            'required': 'Toto pole je povinné.',
            'max_length': 'Používateľské meno nemôže byť dlhšie ako 150 znakov.',
            'invalid': 'Používateľské meno obsahuje neplatné znaky.',
        }
    )
    
    # Customizing password1 field
    password1 = forms.CharField(
        label="Heslo",
        widget=forms.PasswordInput(),  # This masks the password input
        help_text="<br> Heslo musí mať minimálne 8 znakov a nemôže byť rovnaké ako iné osobné údaje.",
        error_messages={
            'required': 'Toto pole je povinné.',
            'min_length': 'Heslo musí mať aspoň 8 znakov.',
        }
    )

    # Customizing password2 field
    password2 = forms.CharField(
        label="Potvrď heslo",
        widget=forms.PasswordInput(),  # This masks the password input
        help_text="<br> Zadajte to isté heslo pre overenie.",
        error_messages={
            'required': 'Toto pole je povinné.',
            'mismatch': 'Heslá sa musia zhodovať.',
            'max_length': 'Heslo je príliš dlhé.',
        }
    )