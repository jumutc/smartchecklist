from django.contrib.auth.models import User
from django.db.models.aggregates import Sum
from django.db import models
from decimal import Decimal

class Tag(models.Model):
    name = models.CharField(max_length=120)
    description = models.CharField(max_length=240, null=True)

class DictionaryCategory(models.Model):
    name = models.CharField(max_length=120)

    def __str__(self):
        return self.name

class DictionaryItem(models.Model):
    name = models.CharField(max_length=120)
    category = models.ForeignKey(DictionaryCategory)
    description = models.CharField(max_length=240, null=True, blank=True)
    price = models.DecimalField(default=Decimal('0.0'), decimal_places=5, max_digits=10)

class CheckList(models.Model):
    creator = models.ForeignKey(User)
    name = models.CharField(max_length=120, null=True)
    description = models.CharField(max_length=240, null=True)
    items = models.ManyToManyField(DictionaryItem)
    creation_time = models.DateTimeField(auto_now_add=True)
    last_update_time = models.DateTimeField(auto_now_add=True, null=True)

    class Meta:
        ordering = ['-creation_time']

    def calculate_total(self):
        return CheckList.objects.filter(id=self.id).aggregate(Sum('items__price')).values()[0]

    total = property(calculate_total)

class Store(models.Model):
    name = models.CharField(max_length=120)
    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return self.name

class PromotedItem(DictionaryItem):
    store = models.ForeignKey(Store)
    expiration_time = models.DateTimeField()

    class Meta:
        ordering = ['-expiration_time']

class HistogramItem(models.Model):
    item_a = models.ForeignKey(DictionaryItem, related_name="histogramitem_a_set")
    item_b = models.ForeignKey(DictionaryItem, related_name="histogramitem_b_set")
    probability = models.DecimalField(default=Decimal('1.0'), decimal_places=5, max_digits=6)

class UserProfile(models.Model):
    user = models.OneToOneField(User)
    checklists = models.ManyToManyField(CheckList)


