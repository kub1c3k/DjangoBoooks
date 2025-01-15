from django.contrib import admin

from .models import Review, Book

class ReviewInline(admin.TabularInline):
    model = Review
    extra = 3


class BookAdmin(admin.ModelAdmin):
    fieldsets = [
        (None, {"fields": ["title"]}),
        ("Author information", {"fields": ["author"]}),
        ("Image information", {"fields": ["image"]}),
        ("Date information", {"fields": ["pub_date"], "classes": ["collapse"]}),
    ]
    inlines = [ReviewInline]
    list_display = ("title", "pub_date", "was_published_recently")
    list_filter = ["pub_date"]
    search_fields = ["title"]


admin.site.register(Book, BookAdmin) 