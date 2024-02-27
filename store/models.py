from django.db import models
from blog.models import BaseModel
# from decimal import Decimal
from django.contrib.auth import get_user_model

UserModel = get_user_model()


class Category(BaseModel):
    name = models.CharField(max_length=255, null=False, blank=False, verbose_name="Name", unique=True)
    description = models.TextField(null=False, blank=False, verbose_name="Description")

    class Meta:
        verbose_name = 'Category'
        verbose_name_plural = 'Categories'
        ordering = ('name', )


    def __str__(self):
        return self.name
    

class Product(BaseModel):
    name = models.CharField(max_length=255, verbose_name="Name", null=False, blank=False,)
    description = models.TextField(verbose_name="Description")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='Category', related_name='products')
    discount = models.PositiveIntegerField(default=0, verbose_name="Discount Percentage")
    thumbnail = models.ImageField(upload_to='media/store/thumbnails/', null=True, blank=True)

    class Meta:
        verbose_name = 'Product'
        verbose_name_plural = 'Products'

    def __str__(self):
        return self.name

    @property
    def price(self):
        return self.prices.filter(is_active=True).last()


class Price(BaseModel):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='prices')
    price = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Price")

    class Meta:
        verbose_name = 'Price'
        verbose_name_plural = 'Prices'

    def __str__(self):
        return f"{self.product.name} - {self.price}"


class Media(BaseModel):
    MEDIA_TYPE = (
        ("image", "Image"),
        ("video", "Video"),
        ("audio", "Audio"),
)
    file = models.FileField(upload_to='media/store/media', verbose_name='File')
    media_type = models.CharField(
        max_length=10, 
        choices=MEDIA_TYPE, 
        default="image", 
        null=False, 
        blank=False,
        verbose_name='Media type'
        )
    title = models.CharField(max_length=255, null=False, blank=False)
    description = models.TextField(null=False, blank=False)
    product = models.ForeignKey(Product, on_delete=models.CASCADE ,verbose_name='Product', related_name='Medias')
    date = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = 'Media'
        verbose_name_plural = 'Medias'

    def __str__(self):
        return self.title
    

class Comment(BaseModel):
    author = models.ForeignKey(UserModel, on_delete=models.PROTECT, verbose_name='User', related_name='Products')
    product = models.ForeignKey(Product, on_delete=models.CASCADE, verbose_name='Product', related_name='Comments')
    text = models.TextField(null=False, blank=False, verbose_name='Comment')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Date')
    approved = models.BooleanField(default=False, verbose_name='Approved')

    class Meta:
        verbose_name = 'Comment'
        verbose_name_plural = 'Comments'

    def __str__(self):
        return f'{self.author.username} - {self.text}'
