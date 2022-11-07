from rest_framework import serializers
from rest_framework.authtoken.models import Token
from user_api.models import *

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = SiteUser
        fields = ('id', 'username', 'email', 'password', 'special_user', 'shipping_address', 'phone_number')
        extra_kwargs = {'password': {'write_only': True, 'required': False}, 'username': {'required': False}, 'email': {'required': False}}
        depth = 1
        
    def create(self, validated_data):
        user = SiteUser(
            username=validated_data['username'],
            email=validated_data['email'],
            password=validated_data['password'],
        )
        user.set_password(validated_data['password'])
        user.save()
        Token.objects.create(user=user)
        return user

class ChangePasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(required=True)
    new_password = serializers.CharField(required=True)
    
    def validate(self, data):
        return data