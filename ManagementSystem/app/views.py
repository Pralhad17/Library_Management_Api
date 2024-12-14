from datetime import datetime
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import CustomUser, Book, BorrowRequest
from .serializers import UserSerializer, BookSerializer, BorrowRequestSerializer

class CreateUserView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class BookListView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_librarian:  # Admin can see all books
            books = Book.objects.all()
        else:  # Regular user can see their own books
            books = Book.objects.filter(user=request.user)

        serializer = BookSerializer(books, many=True)
        return Response(serializer.data)

class BorrowRequestView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user = request.user
        data = request.data
        data['user'] = user.id
        serializer = BorrowRequestSerializer(data=data)
        if serializer.is_valid():
            existing_requests = BorrowRequest.objects.filter(book_id=data['book'], status='Approved')
            for req in existing_requests:
                if req.start_date <= datetime.strptime(data['end_date'], '%Y-%m-%d').date() and req.end_date >= datetime.strptime(data['start_date'], '%Y-%m-%d').date():
                    return Response({"error": "Book already borrowed for selected dates."}, status=status.HTTP_400_BAD_REQUEST)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ApproveDenyRequestView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def put(self, request, request_id):
        try:
            borrow_request = BorrowRequest.objects.get(id=request_id)
            if request.user.is_librarian:
                borrow_request.status = request.data.get('status', borrow_request.status)
                borrow_request.save()
                return Response({"message": "Request updated."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Permission denied."}, status=status.HTTP_403_FORBIDDEN)
        except BorrowRequest.DoesNotExist:
            return Response({"error": "Request not found."}, status=status.HTTP_404_NOT_FOUND)

@api_view(['POST'])
def get_tokens_for_user(request):
    username = request.data.get("username")
    password = request.data.get("password")
    user = authenticate(username=username, password=password)
    
    if user is not None:
        refresh = RefreshToken.for_user(user)
        return Response({
            'refresh': str(refresh),
            'access': str(refresh.access_token),
        })
    else:
        return Response({"error": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)

class UserProfileView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.is_librarian:  # Admin can see all users
            users = CustomUser.objects.all()
        else:  # Regular user can see only their own profile
            users = CustomUser.objects.filter(id=request.user.id)

        user_serializer = UserSerializer(users, many=True)
        return Response(user_serializer.data)

class CreateBookView(APIView):
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def post(self, request):
        # Check if the user is a librarian
        if not request.user.is_librarian:
            return Response({"error": "Permission denied. Only librarians can add books."}, status=status.HTTP_403_FORBIDDEN)
        
        # Serialize the incoming data and validate it
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            # Save the book if data is valid
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        # Return errors if the data is invalid
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)