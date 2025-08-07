from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from .models import Account, Transaction
from .serializers import TransactionSerializer
from rest_framework.response import Response
from rest_framework.decorators import api_view

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
        amount = request.data.get('amount')
        account = Account.objects.get(user=request.user)
        account.balance += float(amount)
        account.save()

        Transaction.objects.create(
            sender=request.user,
            transaction_type='deposit',
            amount=amount
        )
        return Response({"message": "Deposit successful."}, status=status.HTTP_200_OK)

class WithdrawView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        amount = float(request.data.get('amount'))
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

class TransferView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        receiver_username = request.data.get('receiver')
        amount = float(request.data.get('amount'))
        pin = request.data.get('pin')

        try:
            sender_account = Account.objects.get(user=request.user)
            receiver_account = Account.objects.get(user__username=receiver_username)
        except Account.DoesNotExist:
            return Response({"error": "Receiver account not found."}, status=status.HTTP_404_NOT_FOUND)

        if sender_account.pin != pin:
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
