from django.contrib import admin

from .models.account import Account
from .models.category import Category
from .models.transaction import Transaction

admin.site.register(Account)
admin.site.register(Category)
admin.site.register(Transaction)
