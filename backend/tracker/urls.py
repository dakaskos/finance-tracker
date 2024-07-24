from rest_framework.routers import DefaultRouter

from .views.transaction import TransactionViewSet
from .views.account import AccountViewSet
from .views.user import UserViewSet


router = DefaultRouter()
router.register('api/transaction', TransactionViewSet, basename='transaction')
router.register('api/account', AccountViewSet, basename='account')
router.register('api/user', UserViewSet, basename='user')

urlpatterns = router.urls
