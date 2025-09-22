from rest_framework import viewsets, filters, status
from rest_framework.decorators import action, api_view
from rest_framework.response import Response
from rest_framework.reverse import reverse
from django_filters.rest_framework import DjangoFilterBackend
from django.db.models import Q
from .models import Category, Product, ProductImage
from .serializers import (
    CategorySerializer,
    CategoryListSerializer,
    ProductSerializer,
    ProductListSerializer,
    ProductCreateUpdateSerializer,
    ProductImageSerializer,
)


@api_view(["GET"])
def api_root(request, format=None):
    return Response(
        {
            "categories": reverse(
                "products:category-list", request=request, format=format
            ),
            "products": reverse(
                "products:product-list", request=request, format=format
            ),
            "product-images": reverse(
                "products:productimage-list", request=request, format=format
            ),
        }
    )


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Category.objects.filter(is_active=True)
    serializer_class = CategorySerializer
    lookup_field = "slug"
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["parent", "is_active"]
    search_fields = ["name", "description"]
    ordering_fields = ["name", "created_at"]
    ordering = ["name"]

    def get_serializer_class(self):
        if self.action == "list":
            return CategoryListSerializer
        return CategorySerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        if self.request.query_params.get("root_only") == "true":
            queryset = queryset.filter(parent__isnull=True)
        return queryset.select_related("parent").prefetch_related("subcategories")

    @action(detail=True, methods=["get"])
    def products(self, request, slug=None):
        category = self.get_object()
        products = (
            Product.objects.filter(category=category, is_active=True)
            .select_related("category", "seller")
            .prefetch_related("images")
        )

        price_min = request.query_params.get("price_min")
        price_max = request.query_params.get("price_max")
        if price_min:
            products = products.filter(price__gte=price_min)
        if price_max:
            products = products.filter(price__lte=price_max)

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = ProductListSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def tree(self, request):
        root_categories = self.get_queryset().filter(parent__isnull=True)
        serializer = CategorySerializer(
            root_categories, many=True, context={"request": request}
        )
        return Response(serializer.data)


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.filter(is_active=True)
    filter_backends = [
        DjangoFilterBackend,
        filters.SearchFilter,
        filters.OrderingFilter,
    ]
    filterset_fields = ["category", "seller", "featured", "is_active"]
    search_fields = ["title", "description"]
    ordering_fields = ["title", "price", "created_at", "stock_quantity"]
    ordering = ["-created_at"]
    lookup_field = "slug"

    def get_serializer_class(self):
        if self.action == "list":
            return ProductListSerializer
        elif self.action in ["create", "update", "partial_update"]:
            return ProductCreateUpdateSerializer
        return ProductSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        price_min = self.request.query_params.get("price_min")
        price_max = self.request.query_params.get("price_max")
        in_stock = self.request.query_params.get("in_stock")
        category_slug = self.request.query_params.get("category_slug")

        if price_min:
            queryset = queryset.filter(price__gte=price_min)
        if price_max:
            queryset = queryset.filter(price__lte=price_max)
        if in_stock == "true":
            queryset = queryset.filter(stock_quantity__gt=0)
        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)

        return queryset.select_related("category", "seller").prefetch_related("images")

    @action(detail=False, methods=["get"])
    def search(self, request):
        query = request.query_params.get("q", "")
        if not query:
            return Response(
                {"detail": 'Parâmetro de busca "q" é obrigatório.'},
                status=status.HTTP_400_BAD_REQUEST,
            )

        products = self.get_queryset().filter(
            Q(title__icontains=query) | Q(description__icontains=query)
        )
        products = self.filter_queryset(products)

        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = ProductListSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=False, methods=["get"])
    def featured(self, request):
        products = self.get_queryset().filter(featured=True)
        page = self.paginate_queryset(products)
        if page is not None:
            serializer = ProductListSerializer(
                page, many=True, context={"request": request}
            )
            return self.get_paginated_response(serializer.data)
        serializer = ProductListSerializer(
            products, many=True, context={"request": request}
        )
        return Response(serializer.data)

    @action(detail=True, methods=["post"])
    def add_image(self, request, slug=None):
        product = self.get_object()
        if product.seller != request.user:
            return Response(
                {"detail": "Você não tem permissão para editar este produto."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProductImageSerializer(
            data=request.data, context={"request": request}
        )
        if serializer.is_valid():
            serializer.save(product=product)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ProductImageViewSet(viewsets.ModelViewSet):
    queryset = ProductImage.objects.all()
    serializer_class = ProductImageSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ["product", "is_primary"]
    ordering_fields = ["order", "created_at"]
    ordering = ["order", "id"]

    def get_queryset(self):
        return super().get_queryset().select_related("product")
