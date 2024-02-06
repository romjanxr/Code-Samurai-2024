from rest_framework import status
from django.http import JsonResponse
from rest_framework.decorators import api_view
from .models import Book
from .serializers import BookSerializer
from django.db.models import Q

@api_view(['GET', 'POST'])
def create_read_search_book(request):
    if request.method == 'GET':
        title = request.GET.get('title')
        author = request.GET.get('author')
        genre = request.GET.get('genre')
        sorting_field = request.GET.get('sort', 'id')
        sorting_order = request.GET.get('order', 'ASC')
        
        #Validating sorting field
        allowed_sorting_fields = ['title', 'author', 'genre', 'price']
        sorting_field = sorting_field if sorting_field in allowed_sorting_fields else 'id'
        
        # Getting all entries
        queryset = Book.objects.all()
        
        # Now Let's filter
        if title:
            queryset = queryset.filter(title__exact=title)
        if author:
            queryset = queryset.filter(author__exact=author)
        if genre:
            queryset = queryset.filter(genre__exact=genre)

        if sorting_order.upper() == 'DESC':
            sorting_field = f'-{sorting_field}'

        queryset = queryset.order_by(sorting_field, 'id')

        serializer = BookSerializer(queryset, many=True)

        return JsonResponse({'books': serializer.data}, status=status.HTTP_200_OK)
    
    if request.method == 'POST':
        serializer = BookSerializer(data=request.data)

        if serializer.is_valid():
            instance = serializer.save()
            serialized_data = BookSerializer(instance).data
            return JsonResponse(serialized_data, status=status.HTTP_201_CREATED)



@api_view(['GET', 'PUT'])
def fetch_or_update_book(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return JsonResponse({'message': f'book with id: {pk} was not found'}, status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return JsonResponse(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse(serializer.data, status=status.HTTP_200_OK)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    else:
        return JsonResponse({'detail': 'Method not allowed'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)
    