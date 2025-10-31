from rest_framework import generics
from .models import Merchant
from .serializers import MerchantSerializer

class MerchantListView(generics.ListCreateAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer

class MerchantDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
