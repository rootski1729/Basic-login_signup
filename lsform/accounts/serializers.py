from rest_framework import serializers
from .models import CustomUser

class signupserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'user_type', 'profile_pic', 'address_line1', 'city', 'state', 'pincode']
        
    def validate(self,data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': 'password should match'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user
        
class userserializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields='__all__'
    