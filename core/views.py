from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth.models import User
from decimal import Decimal

from .models import Account, Transaction
from .serializers import *

# User Registration
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

# Account Creation
class CreateAccountView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [JWTAuthentication]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

# Set PIN
class SetPinView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        pin = request.data.get('pin')
        if not pin or len(pin) != 4 or not pin.isdigit():
            return Response({"error": "PIN must be exactly 4 digits."}, status=400)
        try:
            account = request.user.account
        except:
            return Response({"error": "Account not found."}, status=404)

        account.set_pin(pin)
        return Response({"message": "PIN set successfully."})

# Balance View
class BalanceView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'account_number'

# Fund Transfer
class TransferFundsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender_acc_num = request.data.get("sender")
        receiver_acc_num = request.data.get("receiver")
        amount = float(request.data.get("amount"))
        pin = request.data.get("pin")

        if not pin:
            return Response({"error": "PIN is required."}, status=400)

        try:
            sender = Account.objects.get(account_number=sender_acc_num, user=request.user)
            receiver = Account.objects.get(account_number=receiver_acc_num)
        except Account.DoesNotExist:
            return Response({"error": "Invalid account number"}, status=400)

        if not sender.check_pin(pin):
            return Response({"error": "Invalid PIN."}, status=403)

        if sender.balance < amount:
            return Response({"error": "Insufficient balance"}, status=400)

        sender.balance -= amount
        receiver.balance += amount
        sender.save()
        receiver.save()

        Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)

        return Response({"message": "Transfer successful"})

# Deposit
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def deposit(request):
    try:
        amount = Decimal(request.data.get("amount", 0))
        if amount <= 0:
            return Response({"error": "Invalid deposit amount"}, status=400)

        account = Account.objects.get(user=request.user)
        account.balance += amount
        account.save()

        Transaction.objects.create(account=account, type='credit', amount=amount, description='Deposit')

        return Response({"message": "Deposit successful", "new_balance": account.balance})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# Withdrawal
@api_view(['POST'])
@permission_classes([IsAuthenticated])
def withdraw(request):
    try:
        amount = Decimal(request.data.get("amount", 0))
        pin = request.data.get("pin", "")
        account = Account.objects.get(user=request.user)

        if not account.check_pin(pin):
            return Response({"error": "Invalid PIN"}, status=403)

        if amount <= 0 or amount > account.balance:
            return Response({"error": "Invalid withdrawal amount"}, status=400)

        account.balance -= amount
        account.save()

        Transaction.objects.create(account=account, type='debit', amount=amount, description='Withdrawal')

        return Response({"message": "Withdrawal successful", "new_balance": account.balance})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

# Transaction History
class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        account = request.user.account
        transactions = Transaction.objects.filter(account=account)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

# Home View
@api_view(['GET'])
def home_view(request):
    return Response({"message": "Welcome to the Banking API"})
