from rest_framework import serializers
from .models import CustomUser
from django import forms

class signupserializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    confirm_password = serializers.CharField(write_only=True)
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'user_type', 'profile_pic', 'address_line1', 'city', 'state', 'pincode']
        
    def validate(self,data):
        if data['password'] != data['confirm_password']:
            raise serializers.ValidationError({'password': 'password should match'})
        
        if CustomUser.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError({'email': 'email already exists'})
        if CustomUser.objects.filter(username=data['username']).exists():
            raise serializers.ValidationError({'username': 'username already exists'})
        return data
    
    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = CustomUser.objects.create_user(**validated_data)
        return user
        
        
        
class signupform(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)
    confirm_password = forms.CharField(widget=forms.PasswordInput)  
    
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'password', 'confirm_password', 'user_type', 'profile_pic', 'address_line1', 'city', 'state', 'pincode']
        
        def clean(self):
            cleaned_data = super().clean()
            password = cleaned_data.get('password')
            confirm_password = cleaned_data.get('confirm_password')
            
            if password != confirm_password:
                raise forms.ValidationError('password should match')
            
            return cleaned_data
class userserializer(serializers.ModelSerializer):
    class Meta:
        model=CustomUser
        fields='__all__'
    