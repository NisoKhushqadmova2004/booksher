from  rest_framework import serializers
from django.contrib.auth.models import User
from .models import Profile


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only =True)
    password2 = serializers.CharField(write_only =True)

    class Meta:
        model = User
        fields = ['username','email','password','password2']

    def validate(self, data):
        if data['password'] != data['password2']:
            raise serializers.ValidationError('пароль не совпадают')
        return data
    def create(self, validated_data):
        validated_data.pop('password2')

        user = User.objects.create_user( username=validated_data['username'],email=validated_data['email'],
        password=validated_data['password'])

        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = Profile
        fields = ['username', 'email', 'name', 'city']

