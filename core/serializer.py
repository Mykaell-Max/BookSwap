from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Book, BookExchange


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
        # Tenta obter o perfil criado automaticamente pelo signal; se não existir, cria
        profile, created = UserProfile.objects.get_or_create(user=user)
        # Atualiza os campos do perfil com os dados enviados
        profile.city = profile_data.get('city', profile.city)
        profile.neighborhood = profile_data.get('neighborhood', profile.neighborhood)
        profile.phone = profile_data.get('phone', profile.phone)
        profile.save()
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


class BookSerializer(serializers.ModelSerializer):
    owner = serializers.ReadOnlyField(source='owner.username')

    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'genre', 'owner', 'created_at']


class BookExchangeSerializer(serializers.ModelSerializer):
    requester = serializers.ReadOnlyField(source='requester.username')
    receiver = serializers.ReadOnlyField(source='receiver.username')
    requested_book = BookSerializer(read_only=True)
    offered_book = BookSerializer(read_only=True)
    
    requested_book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='requested_book', write_only=True)
    offered_book_id = serializers.PrimaryKeyRelatedField(queryset=Book.objects.all(), source='offered_book', write_only=True)
    receiver_id = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), source='receiver', write_only=True)

    class Meta:
        model = BookExchange
        fields = [
            'id', 'requester', 'receiver', 'requested_book', 'offered_book',
            'requested_book_id', 'offered_book_id', 'receiver_id',
            'status', 'created_at' ]
        
    
    def validate(self, data):
        requester = self.context['request'].user
        
        offered_book = data['offered_book_id']  

        if offered_book.owner != requester:
            raise serializers.ValidationError('You can only offer books you own!')

        return data


    def update(self, instance, validated_data):
        request = self.context["request"] 

        if "status" in validated_data:
            if request.user != instance.receiver:
                raise serializers.ValidationError("Only the receiver can accpept or decline an offer!")

        return super().update(instance, validated_data)