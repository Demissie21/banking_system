from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from django.contrib.auth.hashers import check_password
from .models import Account, Transaction
from .serializers import DepositSerializer, WithdrawSerializer, TransferSerializer
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import check_password
from .models import Account, Transaction
from .serializers import TransactionSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
class TransferFundsView(APIView):
    authentication_classes = [SessionAuthentication]  # or JWT if you're using it
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender = get_object_or_404(Account, user=request.user)
        ...

class TransferFundsView(APIView):
    def post(self, request):
        sender = get_object_or_404(Account, user=request.user)
        receiver_id = request.data.get("receiver_id")
        amount = float(request.data.get("amount", 0))
        pin = request.data.get("pin")

        if not check_password(pin, sender.pin):
            return Response({"error": "Invalid PIN"}, status=status.HTTP_403_FORBIDDEN)

        if amount <= 0 or sender.balance < amount:
            return Response({"error": "Insufficient funds or invalid amount"}, status=status.HTTP_400_BAD_REQUEST)

        receiver = get_object_or_404(Account, id=receiver_id)

        # Transfer funds
        sender.balance -= amount
        receiver.balance += amount
        sender.save()
        receiver.save()

        # Save transaction
        transaction = Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)

        return Response(TransactionSerializer(transaction).data, status=status.HTTP_201_CREATED)

@api_view(['GET'])
def api_root(request):
    return Response({
        "Deposit": "/api/deposit/",
        "Withdraw": "/api/withdraw/",
        "Transfer": "/api/transfer/"
    })

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
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

            # Secure PIN check
            if not check_password(pin, sender_account.pin):
                return Response({"error": "Invalid PIN."}, status=status.HTTP_403_FORBIDDEN)

            if sender_account.balance < amount:
                return Response({"error": "Insufficient funds."}, status=status.HTTP_400_BAD_REQUEST)

            # Transfer logic
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
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
