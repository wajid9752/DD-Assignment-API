from rest_framework.authtoken.models import Token
from rest_framework import serializers
from account.models import User
from django.contrib.auth import authenticate


class LoginSerializer(serializers.Serializer):
    email = serializers.CharField()
    password = serializers.CharField(write_only=True)

    def validate(self, data):
        user = authenticate(
            email=data.get('email'),
            password=data.get('password')
        )
        if not user or not user.is_active:
            raise serializers.ValidationError("Incorrect credentials. Please try again.")

        data['user'] = user
        return data


class UserSerializer(serializers.ModelSerializer):
    token = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ('id', 'username', 'email','role','active', 'token',)

    def get_token(self, obj):
        token, created = Token.objects.get_or_create(user=obj)
        return token.key