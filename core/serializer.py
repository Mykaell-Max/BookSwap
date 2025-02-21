from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['city', 'neighborhood', 'phone']


class UserSerializer(serializers.ModelSerializer):
    profile = UserProfileSerializer() 

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password', 'profile']
        extra_kwargs = {'password': {'write_only': True}} 

    def create(self, validated_data):
        profile_data = validated_data.pop('profile', {})
        user = User.objects.create_user(**validated_data)
        UserProfile.objects.create(user=user, **profile_data)

        return user

    def update(self, instance, validated_data):
        profile_data = validated_data.pop('profile', {})
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.set_password(validated_data.get('password', instance.password))
        instance.save()

        profile = instance.profile
        profile.city = profile_data.get('city', profile.city)
        profile.neighborhood = profile_data.get('neighborhood', profile.neighborhood)
        profile.phone = profile_data.get('phone', profile.phone)
        profile.save()

        return instance