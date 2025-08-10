from rest_framework import serializers
from .models import Account, Transaction
from rest_framework import serializers
from .models import Transaction, Account

class TransactionSerializer(serializers.ModelSerializer):
    sender_username = serializers.CharField(source='sender.user.username', read_only=True)
    receiver_username = serializers.CharField(source='receiver.user.username', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'sender', 'sender_username', 'receiver', 'receiver_username', 'amount', 'timestamp']
        read_only_fields = ['timestamp']

class DepositSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=0.01)

class WithdrawSerializer(serializers.Serializer):
    amount = serializers.FloatField(min_value=0.01)

class TransferSerializer(serializers.Serializer):
    receiver = serializers.CharField()
    amount = serializers.FloatField(min_value=0.01)
    pin = serializers.CharField()

class AccountSerializer(serializers.ModelSerializer):
    class Meta:
        model = Account
        fields = ['id', 'user', 'balance', 'pin']

class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = '__all__'
