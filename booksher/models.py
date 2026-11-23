from django.db import models
from django.conf import settings


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class City(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Book(models.Model):

    CONDITION_CHOICES = (
        ('new', 'New'),
        ('good', 'Good'),
        ('average', 'Average'),
        ('bad', 'Bad'),
    )

    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    title = models.CharField(max_length=40)
    author = models.CharField(max_length=30)
    description = models.TextField()
    status = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    is_free = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Trade(models.Model):

    STATUS = (
        ('pending', 'Pending'),
        ('rejected', 'Rejected'),
        ('accepted', 'Accepted'),
        ('returned', 'Returned'),
    )

    book = models.CharField(max_length=20)
    getter = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    treade_at = models.DateTimeField(auto_now=True)
    start_data = models.DateTimeField()
    finish = models.CharField(max_length=50)
    status = models.CharField(max_length=50, choices=STATUS)

    def __str__(self):
        return self.status
