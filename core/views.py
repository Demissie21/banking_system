from rest_framework import generics, status
from rest_framework.response import Response
from .models import Account, Transaction
from .serializers import *
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.response import Response
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Transaction
from .serializers import TransactionSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework import serializers
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Account
from decimal import Decimal

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

        return Response({"message": "Deposit successful", "new_balance": account.balance})
    except Exception as e:
        return Response({"error": str(e)}, status=500)

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

        return Response({"message": "Withdrawal successful", "new_balance": account.balance})
    except Exception as e:
        return Response({"error": str(e)}, status=500)



class CreateAccountSerializer(serializers.Serializer):
    account_number = serializers.CharField(max_length=20)

class CreateAccountView(APIView):
    authentication_classes = [JWTAuthentication]
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer = CreateAccountSerializer(data=request.data)
        if serializer.is_valid():
            account_number = serializer.validated_data['account_number']
            if Account.objects.filter(account_number=account_number).exists():
                return Response({"error": "Account number already exists."}, status=400)
            
            account = Account.objects.create(
                user=request.user,
                account_number=account_number,
                balance=0.00
            )
            return Response({"message": "Account created successfully.", "account_number": account.account_number}, status=201)
        return Response(serializer.errors, status=400)


class RegisterUserView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        if not username or not password:
            return Response({"error": "Username and password required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username=username).exists():
            return Response({"error": "Username already exists"}, status=status.HTTP_400_BAD_REQUEST)
        
        user = User.objects.create_user(username=username, password=password)
        return Response({"message": "User created successfully"}, status=status.HTTP_201_CREATED)


class TransactionHistoryView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        # You can modify the filter to include both sender and receiver
        transactions = Transaction.objects.filter(sender=request.user.account)
        serializer = TransactionSerializer(transactions, many=True)
        return Response(serializer.data)

@api_view(['GET'])
def home_view(request):
    return Response({"message": "Welcome to the Banking API"})
class TransferFundsView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        sender_acc_num = request.data.get("sender")
        receiver_acc_num = request.data.get("receiver")
        amount = float(request.data.get("amount"))

        try:
            sender = Account.objects.get(account_number=sender_acc_num, user=request.user)
            receiver = Account.objects.get(account_number=receiver_acc_num)
        except Account.DoesNotExist:
            return Response({"error": "Invalid account number"}, status=400)

        if sender.balance < amount:
            return Response({"error": "Insufficient balance"}, status=400)

        sender.balance -= amount
        receiver.balance += amount
        sender.save()
        receiver.save()

        Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)

        return Response({"message": "Transfer successful"})

class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class CreateAccountView(generics.CreateAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer

class BalanceView(generics.RetrieveAPIView):
    queryset = Account.objects.all()
    serializer_class = AccountSerializer
    lookup_field = 'account_number'

class TransferFundsView(generics.CreateAPIView):
    serializer_class = TransactionSerializer

    def post(self, request, *args, **kwargs):
        sender_acc_num = request.data.get("sender")
        receiver_acc_num = request.data.get("receiver")
        amount = float(request.data.get("amount"))

        try:
            sender = Account.objects.get(account_number=sender_acc_num)
            receiver = Account.objects.get(account_number=receiver_acc_num)
        except Account.DoesNotExist:
            return Response({"error": "Invalid account number"}, status=400)

        if sender.balance < amount:
            return Response({"error": "Insufficient balance"}, status=400)

        sender.balance -= amount
        receiver.balance += amount
        sender.save()
        receiver.save()

        Transaction.objects.create(sender=sender, receiver=receiver, amount=amount)

        return Response({"message": "Transfer successful"})
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
