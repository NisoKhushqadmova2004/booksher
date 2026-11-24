from rest_framework import generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Category, City, Book, Trade, Review
from .serialaizers import *
from .filters import BookFilter
from django_filters.rest_framework import DjangoFilterBackend
from .permissions import IsBookOwner, IsTradeParticipant
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework import status
from django.shortcuts import get_object_or_404

class CategoryListCreateView(generics.ListCreateAPIView):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class CityListCreateView(generics.ListCreateAPIView):
    queryset = City.objects.all()
    serializer_class = CitySerializer


class BookListCreateView(generics.ListCreateAPIView):
    queryset = Book.objects.filter(is_free=True)
    serializer_class = BookSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_class = BookFilter

    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return [AllowAny()]

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)


class BookDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer
    permission_classes = [IsBookOwner]


class TradeListCreateView(generics.ListCreateAPIView):
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Trade.objects.filter(sender=self.request.user) | Trade.objects.filter(getter=self.request.user)


class TradeDetailView(generics.RetrieveUpdateDestroyAPIView):
    serializer_class = TradeSerializer
    permission_classes = [IsAuthenticated, IsTradeParticipant]

    def get_queryset(self):
        return Trade.objects.filter(sender=self.request.user) | Trade.objects.filter(getter=self.request.user)

class MyBooksView(generics.ListAPIView):
    serializer_class = BookSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Book.objects.filter(owner=self.request.user)    

class ReviewListCreateView(generics.ListCreateAPIView):
    serializer_class = ReviewSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Review.objects.all()

    def perform_create(self, serializer):
        serializer.save(reviewer=self.request.user) 


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def accept_trade(request, pk):
    trade = get_object_or_404(Trade, pk=pk)
    if trade.getter != request.user:
        return Response({'error': 'Шумо иҷозати қабул кардани ин дархостро надоред!'},status=status.HTTP_403_FORBIDDEN)

    if trade.status != 'pending':
        return Response({'error': 'Ин дархост дигар pending нест!'},status=status.HTTP_400_BAD_REQUEST)

    trade.status = 'accepted'
    trade.save()

    trade.requested_book.is_exchanged = True
    trade.requested_book.save()

    trade.offered_book.is_exchanged = True
    trade.offered_book.save()

    Trade.objects.filter(status='pending',requested_book__in=[trade.requested_book, trade.offered_book]).exclude(pk=trade.pk).update(status='rejected')
    Trade.objects.filter(status='pending',offered_book__in=[trade.requested_book, trade.offered_book]).exclude(pk=trade.pk).update(status='rejected')

    return Response({'message': 'Мубодила қабул карда шуд!'})    

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def reject_trade(request, pk):
    trade = get_object_or_404(Trade, pk=pk)

    if trade.getter != request.user:
        return Response({'error': 'Шумо иҷозати рад кардани ин дархостро надоред!'},status=status.HTTP_403_FORBIDDEN)

    if trade.status != 'pending':
        return Response({'error': 'Ин дархост дигар pending нест!'},status=status.HTTP_400_BAD_REQUEST)

    trade.status = 'rejected'
    trade.save()

    return Response({'message': 'Дархост рад карда шуд!'})       