from django.urls import path
from .views import DepositView, WithdrawView, TransferView
from .views import DepositView, WithdrawView, TransferView, api_root
urlpatterns = [
    path('', api_root),
    path('deposit/', DepositView.as_view()),
    path('withdraw/', WithdrawView.as_view()),
    path('transfer/', TransferView.as_view()),
]
