from enum import Enum

from django.db import models
from django.conf import settings


class TransactionType(Enum):
    INCOME = 1
    EXPENSE = -1


class Transaction(models.Model):
    objects = None
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    account = models.ForeignKey("Account", on_delete=models.CASCADE, default=None)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True, null=True)
    date = models.DateField()
    type = models.IntegerField(
        choices=[(tag.value, tag.name) for tag in TransactionType]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.amount} - {self.amount.name}"
