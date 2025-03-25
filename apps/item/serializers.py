from rest_framework import serializers
from .models import Item, ItemList
from django.contrib.auth.models import User 
from authentication.serializers import UserSerializer

class ItemSerializer(serializers.ModelSerializer):
    
    responsible = UserSerializer(read_only=True)
    responsible_id = serializers.PrimaryKeyRelatedField(
        queryset = User.objects.all(),
        source = 'responsible',
        write_only = True,
        required = False,
        allow_null = True
    )

    class Meta:
        model = Item
        fields = ['id', 'name', 'responsible', 'resposible_id', 'status', 'added_at', 'updated_at']
        read_only_fields = ['added_at', 'updated_at']

        
class ItemListSerializer(serializers.ModelSerializer):
    
    items = ItemSerializer(many=True, read_only=True)

    class Meta:
        model = ItemList
        fields = ['id', 'title', 'description', 'items']