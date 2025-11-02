from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated
from .models import Merchant
from .serializers import MerchantSerializer

class MerchantViewSet(ModelViewSet):
    queryset = Merchant.objects.all()
    serializer_class = MerchantSerializer
    permission_classes = [IsAuthenticated]

# class MerchantDetailView(generics.RetrieveUpdateDestroyAPIView):
#     queryset = Merchant.objects.all()
#     serializer_class = MerchantSerializer
