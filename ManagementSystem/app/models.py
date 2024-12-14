from django.contrib.auth.models import AbstractUser
from django.db import models

class CustomUser(AbstractUser):
    is_librarian = models.BooleanField(default=False)  # True for admin or librarian

    def __str__(self):
        return self.username


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    
    @property
    def unique_id(self):
        return f"{self.id}-{self.title[:5]}"  # Example of creating a unique_id based on book's ID and title
    
    def __str__(self):
        return self.title


class BorrowRequest(models.Model):
    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    status = models.CharField(max_length=50, default='Pending')

    def __str__(self):
        return f'{self.book.title} - {self.status}'
