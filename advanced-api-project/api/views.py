from django_filters import rest_framework
from rest_framework import generics
from rest_framework.permissions import IsAuthenticatedOrReadOnly, IsAuthenticated, AllowAny
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework import filters
from .models import Book
from .serializers import BookSerializer






# Create your views here.
class BookListView(generics.ListAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    
    filter_backends = [DjangoFilterBackend, SearchFilter, filters.OrderingFilter]

    filterset_fields = ["title","author","publication_year"]
    search_fields = ["title", "author"]
    ordering_fields = ["title", "author", "publication_year"]



class BookDetailView(generics.RetrieveAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [AllowAny]
    #lookup_field = "id"

class BookCreateView(generics.CreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes =[IsAuthenticated]
    
    def perform_create(self, serializer):
        serializer.save()
    

class BookUpdateView(generics.UpdateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        queryset = Book.objects.all()
        title = self.request.query_params.get("title")
        if title:
            queryset = queryset.filter(title__icontains=title)
            
        return queryset
    
    def perform_update(self, serializer):
        serializer.save()
    #lookup_field = "id"

class BookDeleteView(generics.DestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    lookup_field = "id"