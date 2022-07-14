from django.contrib.auth.models import User
from django.db import models

from products.models import Product
from django.utils.crypto import get_random_string
from django.utils.text import slugify


CODE_LENGTH = 11
def generate_id_length():
    return get_random_string(CODE_LENGTH).upper()

class Order(models.Model):
    user = models.ForeignKey(User, related_name='orders', on_delete=models.CASCADE)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.CharField(max_length=100)
    address = models.CharField(max_length=100)
    zipcode = models.CharField(max_length=100)
    place = models.CharField(max_length=100)
    phone = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    paid_amount = models.DecimalField(max_digits=8, decimal_places=2, blank=True, null=True)
    coupon = models.CharField(max_length=50, blank=True, null=True)
    code_no = models.CharField(max_length=CODE_LENGTH, editable=False, default="", unique=True)
    
    class Meta:
        ordering = ['-created_at',]
    
    def __str__(self):
        return self.first_name

    def save(self, *args, **kwargs):
        self.code_no = generate_id_length()
        super(Order, self).save(*args, **kwargs)        

class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, related_name='items', on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=8, decimal_places=2)
    quantity = models.IntegerField(default=1)
    slug = models.SlugField(null=True, blank=True, max_length=255, unique=True)

    def __str__(self):
        return '%s' % self.id

    def get_absolute_url(self):
        return f'/order-detail/{self.slug}/'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.product.name + self.order.code_no)
        elif self.slug != slugify(self.product.name + self.order.code_no):
            self.slug = slugify(self.product.name + self.order.code_no)
        super(OrderItem, self).save(*args, **kwargs)        