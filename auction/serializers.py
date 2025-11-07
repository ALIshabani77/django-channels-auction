

from rest_framework import serializers
from .models import AuctionItem

class AuctionItemSerializer(serializers.ModelSerializer):
    is_active = serializers.ReadOnlyField() 

    class Meta:
        model = AuctionItem
        fields = [
            'id', 
            'name', 
            'description', 
            'current_price', 
            'ends_at',
            'is_active', 
            'updated_at'
        ]
