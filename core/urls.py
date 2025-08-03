from django.urls import path
from .views import (
    RegisterUserView,
    CreateAccountView,
    BalanceView,
    TransferFundsView,
    TransactionHistoryView,
    SetPinView,
    deposit,
    withdraw,
    home_view,
)

urlpatterns = [
    path('', home_view),
    path('register/', RegisterUserView.as_view()),
    path('account/create/', CreateAccountView.as_view()),  # ✅ Fix here
    path('account/<str:account_number>/', BalanceView.as_view()),
    path('transfer/', TransferFundsView.as_view()),
    path('transactions/', TransactionHistoryView.as_view()),
    path('account/set-pin/', SetPinView.as_view()),
    path('account/deposit/', deposit),
    path('account/withdraw/', withdraw),
]
