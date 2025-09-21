from django.db import models
from django.contrib.auth.models import User
from django.utils.text import slugify
from django.core.validators import MinValueValidator
from decimal import Decimal


class Category(models.Model):
   
    name = models.CharField(
        max_length=100,
        verbose_name="Nome da Categoria",
        help_text="Nome da categoria de produtos"
    )
    description = models.TextField(
        blank=True,
        null=True,
        verbose_name="Descrição",
        help_text="Descrição detalhada"
    )
    parent = models.ForeignKey(
        'self',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
        related_name='subcategories',
        verbose_name="Categoria Pai",
        help_text="Categoria pai para criar hierarquia"
    )
    slug = models.SlugField(
        max_length=120,
        unique=True,
        blank=True,
        verbose_name="URL Amigável",
        help_text="URL amigável gerada automaticamente"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Define se a categoria está ativa"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )

    class Meta:
        verbose_name = "Categoria"
        verbose_name_plural = "Categorias"
        ordering = ['name']

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
       
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_full_path(self):
        
        path = [self.name]
        parent = self.parent
        while parent:
            path.append(parent.name)
            parent = parent.parent
        return ' > '.join(reversed(path))

    def get_children(self):
        
        return self.subcategories.filter(is_active=True)


class Product(models.Model):
    
    title = models.CharField(
        max_length=200,
        verbose_name="Título do Produto",
        help_text="Título principal do produto"
    )
    description = models.TextField(
        verbose_name="Descrição",
        help_text="Descrição detalhada do produto"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(Decimal('0.01'))],
        verbose_name="Preço",
        help_text="Preço do produto em reais"
    )
    stock_quantity = models.PositiveIntegerField(
        default=0,
        verbose_name="Quantidade em Estoque",
        help_text="Quantidade disponível em estoque"
    )
    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name='products',
        verbose_name="Categoria",
        help_text="Categoria do produto"
    )
    seller = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='products',
        verbose_name="Vendedor",
        help_text="Usuário vendedor do produto"
    )
    slug = models.SlugField(
        max_length=220,
        unique=True,
        blank=True,
        verbose_name="URL Amigável",
        help_text="URL amigável gerada automaticamente"
    )
    is_active = models.BooleanField(
        default=True,
        verbose_name="Ativo",
        help_text="Define se o produto está ativo e visível"
    )
    featured = models.BooleanField(
        default=False,
        verbose_name="Produto em Destaque",
        help_text="Define se o produto aparece em destaque"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Criação"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        verbose_name="Data de Atualização"
    )

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
        ordering = ['-created_at']
        indexes = [
            models.Index(fields=['category', 'is_active']),
            models.Index(fields=['seller', 'is_active']),
            models.Index(fields=['featured', 'is_active']),
            models.Index(fields=['price']),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
       
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)

    @property
    def is_in_stock(self):
       
        return self.stock_quantity > 0

    @property
    def primary_image(self):
        
        return self.images.filter(is_primary=True).first()

    def get_all_images(self):
        
        return self.images.all().order_by('order', 'id')


class ProductImage(models.Model):
    
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name='images',
        verbose_name="Produto",
        help_text="Produto da qual a imagem pertence"
    )
    image = models.ImageField(
        upload_to='products/images/',
        verbose_name="Imagem",
        help_text="Arquivo de imagem do produto"
    )
    alt_text = models.CharField(
        max_length=200,
        blank=True,
        verbose_name="Texto Alternativo",
        help_text="Texto alternativo acessivel"
    )
    is_primary = models.BooleanField(
        default=False,
        verbose_name="Imagem Principal",
        help_text="Define se esta é a imagem principal do produto"
    )
    order = models.PositiveIntegerField(
        default=0,
        verbose_name="Ordem",
        help_text="Ordem de exibição da imagem"
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name="Data de Upload"
    )

    class Meta:
        verbose_name = "Imagem do Produto"
        verbose_name_plural = "Imagens dos Produtos"
        ordering = ['order', 'id']

    def __str__(self):
        return f"Imagem de {self.product.title}"

    def save(self, *args, **kwargs):
        
        if self.is_primary:
            
            ProductImage.objects.filter(
                product=self.product,
                is_primary=True
            ).exclude(id=self.id).update(is_primary=False)
        super().save(*args, **kwargs)