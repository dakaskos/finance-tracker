from rest_framework.routers import DefaultRouter

from .views.transaction import TransactionViewSet
from .views.account import AccountViewSet


router = DefaultRouter()
router.register('api/transaction', TransactionViewSet, basename='transaction')
router.register('api/account', AccountViewSet, basename='account')
urlpatterns = router.urls
