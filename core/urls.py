from django.urls import path
from .views import (
    DepositView,
    WithdrawView,
    TransferView,
    TransactionHistoryView,
    api_root
)

urlpatterns = [
    path('', api_root, name='api-root'),
    path('deposit/', DepositView.as_view(), name='deposit'),
    path('withdraw/', WithdrawView.as_view(), name='withdraw'),
    path('transfer/', TransferView.as_view(), name='transfer'),
    path('transactions/', TransactionHistoryView.as_view(), name='transactions'),
]
