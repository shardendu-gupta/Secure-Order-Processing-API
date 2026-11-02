from rest_framework import serializers
from .models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class RegistrationSerializer(serializers.ModelSerializer):

    password = serializers.CharField(write_only=True, min_length=8)

    class Meta:
        model = User
        fields = ['id', 'username', 'email' ,'password']


    def create(self, validated_data):
        user = User.objects.create_user(username=validated_data['username'], 
                                        email=validated_data['email'], 
                                        password=validated_data['password'])
        return user

                                

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):

    def validate(self, attrs):
        data = super().validate(attrs)

        data['user'] = {'id': self.user.id, 'username': self.user.username, 'email': self.user.email, "role": self.user.role}
        
        return data
