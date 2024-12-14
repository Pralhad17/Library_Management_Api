from django.contrib import admin
from .models import CustomUser, Book, BorrowRequest

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'email', 'is_librarian')
    list_filter = ('is_librarian',)
    search_fields = ('username', 'email')

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'unique_id')
    search_fields = ('title', 'author', 'unique_id')

@admin.register(BorrowRequest)
class BorrowRequestAdmin(admin.ModelAdmin):
    list_display = ('user', 'book', 'start_date', 'end_date', 'status')
    list_filter = ('status',)
    search_fields = ('user__username', 'book__title')

