from rest_framework.routers import DefaultRouter

from .views.transaction import TransactionViewSet
from .views.account import AccountViewSet
from .views.category import CategoryViewSet


router = DefaultRouter()
router.register('api/transaction', TransactionViewSet, basename='transaction')
router.register('api/account', AccountViewSet, basename='account')
router.register('api/category', CategoryViewSet, basename='category')
urlpatterns = router.urls
