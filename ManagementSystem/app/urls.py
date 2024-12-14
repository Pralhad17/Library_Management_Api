from django.urls import path
from .views import CreateUserView, BookListView, BorrowRequestView, ApproveDenyRequestView, get_tokens_for_user, UserProfileView,CreateBookView

urlpatterns = [
    path('create/', CreateUserView.as_view(), name='create_user'),
    path('books/create/', CreateBookView.as_view(), name='create_book'),
    path('login/', get_tokens_for_user, name='login'),
    path('books/', BookListView.as_view(), name='book_list'),
    path('borrow/', BorrowRequestView.as_view(), name='borrow_request'),
    path('borrow/<int:request_id>/', ApproveDenyRequestView.as_view(), name='approve_deny_request'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
]
