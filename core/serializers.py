from rest_framework import serializers
from .models import Account, Transaction
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
