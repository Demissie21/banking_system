from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.decorators import api_view
from django.contrib.auth.hashers import check_password
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from django.http import HttpResponse

from .models import Account, Transaction
from .serializers import DepositSerializer, WithdrawSerializer, TransferSerializer, TransactionSerializer
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render, redirect

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # redirect to login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# Home Page
def home_view(request):
    return HttpResponse("Welcome to the Banking System!")

# User Registration
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})

# API Root
@api_view(['GET'])
def api_root(request):
    return Response({
        "Deposit": "/api/deposit/",
        "Withdraw": "/api/withdraw/",
        "Transfer": "/api/transfer/",
        "Transactions": "/api/transactions/"
    })

# Deposit
class DepositView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = DepositSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            account = Account.objects.get(user=request.user)
            account.balance += amount
            account.save()

            Transaction.objects.create(
                sender=request.user,
                transaction_type='deposit',
                amount=amount
            )
            return Response({"message": "Deposit successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Withdraw
class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = WithdrawSerializer(data=request.data)
        if serializer.is_valid():
            amount = serializer.validated_data['amount']
            account = Account.objects.get(user=request.user)

            if account.balance >= amount:
                account.balance -= amount
                account.save()

                Transaction.objects.create(
                    sender=request.user,
                    transaction_type='withdraw',
                    amount=amount
                )
                return Response({"message": "Withdrawal successful."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Transfer
class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = TransferSerializer(data=request.data)
        if serializer.is_valid():
            receiver_username = serializer.validated_data['receiver']
            amount = serializer.validated_data['amount']
            pin = serializer.validated_data['pin']

            try:
                sender_account = Account.objects.get(user=request.user)
                receiver_account = Account.objects.get(user__username=receiver_username)
            except Account.DoesNotExist:
                return Response({"error": "Receiver account not found."}, status=status.HTTP_404_NOT_FOUND)

            if not check_password(pin, sender_account.pin):
                return Response({"error": "Invalid PIN."}, status=status.HTTP_403_FORBIDDEN)

            if sender_account.balance < amount:
                return Response({"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)

            sender_account.balance -= amount
            receiver_account.balance += amount
            sender_account.save()
            receiver_account.save()

            Transaction.objects.create(
                sender=request.user,
                receiver=receiver_account.user,
                transaction_type='transfer',
                amount=amount
            )

            return Response({"message": "Transfer successful."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

# Transaction History
class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.filter(
            sender=request.user
        ) | Transaction.objects.filter(
            receiver=request.user
        )
        transactions = transactions.order_by('-id')
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)
