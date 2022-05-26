from io import BytesIO
from PIL import Image

from django.core.files import File
from django.db import models
from django.utils.text import slugify
from django.utils.crypto import get_random_string


class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return f'/{self.slug}/'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        elif self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super(Category, self).save(*args, **kwargs)


class Section(models.Model):
    category = models.ForeignKey(
        Category, related_name='sectioncategory', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} | {self.category.name}'

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.slug}/'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.category.slug} {self.name}')
        elif self.slug != slugify(f'{self.category.slug} {self.name}'):
            self.slug = slugify(f'{self.category.slug} {self.name}')
        super(Section, self).save(*args, **kwargs)


class Item(models.Model):
    category = models.ForeignKey(
        Category, related_name='itemcategory', on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section, related_name='itemsection', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, max_length=255, unique=True)

    class Meta:
        ordering = ('name',)

    def __str__(self):
        return f'{self.name} | {self.section.name}'

    def get_absolute_url(self):
        return f'/{self.category.slug}/{self.section.slug}/{self.slug}/'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(f'{self.category.slug} {self.name}')
        elif self.slug != slugify(f'{self.category.slug} {self.name}'):
            self.slug = slugify(f'{self.category.slug} {self.name}')
        super(Item, self).save(*args, **kwargs)


CODE_LENGTH = 7


def generate_id_length():
    return get_random_string(CODE_LENGTH).upper()


class Product(models.Model):
    category = models.ForeignKey(
        Category, related_name='productcategory', on_delete=models.CASCADE)
    section = models.ForeignKey(
        Section, related_name='productsection',  on_delete=models.CASCADE)
    item = models.ForeignKey(
        Item, related_name='productitem', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    slug = models.SlugField(null=True, blank=True, max_length=255, unique=True)
    description = models.TextField(blank=True, null=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    price_before_discount = models.DecimalField(
        max_digits=6, decimal_places=2, blank=True, null=True)
    image = models.ImageField(upload_to='uploads/', blank=True, null=True)
    thumbnail = models.ImageField(upload_to='uploads/', blank=True, null=True)
    date_added = models.DateTimeField(auto_now_add=True)
    in_stock = models.BooleanField(default=True)
    code = models.CharField(max_length=CODE_LENGTH,
                            editable=False, default="", unique=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return f'{self.name} | {self.item.name} | {self.section.name} | {self.category.name}'

    def get_absolute_url(self):
        return f'/{self.slug}/'

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        elif self.slug != slugify(self.name):
            self.slug = slugify(self.name)
        super(Product, self).save(*args, **kwargs)

    def save(self, *args, **kwargs):
        self.code = generate_id_length()
        super(Product, self).save(*args, **kwargs)

    @property
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''

    @property
    def get_thumbnail(self):
        if self.thumbnail:
            return 'http://127.0.0.1:8000' + self.thumbnail.url
        else:
            if self.image:
                self.thumbnail = self.make_thumbnail(self.image)
                self.save()

                return 'http://127.0.0.1:8000' + self.thumbnail.url
            else:
                return ''

    def make_thumbnail(self, image, size=(300, 200)):
        img = Image.open(image)
        img.convert('RGB')
        img.thumbnail(size)

        thumb_io = BytesIO()
        img.save(thumb_io, 'JPEG', quality=85)

        thumbnail = File(thumb_io, name=image.name)

        return thumbnail


class ProductImage(models.Model):
    product = models.ForeignKey(
        Product, related_name='imageproduct', on_delete=models.CASCADE)
    date_added = models.DateTimeField(auto_now_add=True)
    image = models.ImageField(
        upload_to='uploads/productsImages/', blank=True, null=True)

    class Meta:
        ordering = ('-date_added',)

    def __str__(self):
        return self.product.name

    @property
    def get_image(self):
        if self.image:
            return 'http://127.0.0.1:8000' + self.image.url
        return ''
