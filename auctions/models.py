from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    name = models.CharField(max_length=64)

    def __str__(self):
        return f"{self.name}"

class Listing(models.Model):
    title = models.CharField(max_length=64)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="category")
    photo = models.CharField(max_length=200, blank=True)
    description = models.CharField(max_length=200)
    price = models.IntegerField()
    available = models.BooleanField()
    seller = models.ForeignKey(User, models.CASCADE, related_name="seller", null=True)
    wachtlist = models.ManyToManyField(User, blank=True, related_name="listings")
    
    def __str__(self):
        return f"{self.seller}: {self.title}  {self.price}$"


class Bid(models.Model):
    price = models.IntegerField()
    date = models.DateTimeField()
    buyer = models.ForeignKey(User, models.CASCADE, related_name="buyer")
    listing = models.ForeignKey(Listing, models.CASCADE, related_name="bidListing")

    def __str__(self):
        return f"{self.buyer}: {self.price} - {self.listing}$"

class Comment(models.Model):
    text = models.CharField(max_length=200)
    listing = models.ForeignKey(Listing, models.CASCADE, related_name="commentListing")
    user = models.ForeignKey(User, models.CASCADE, related_name="commentUser")
    
