from django.conf import settings
from django.db import models

from ..entities.currency import Currency


class Account(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    currency = models.CharField(
        max_length=3,
        choices=[(tag, tag.value) for tag in Currency]
    )
    is_cash = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.currency} - {self.balance}"
