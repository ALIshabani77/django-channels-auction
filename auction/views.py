from rest_framework.views import APIView
from rest_framework.generics import ListAPIView
from rest_framework.response import Response
from rest_framework import status
from django.db import transaction
from django.utils import timezone
from .models import AuctionItem
from .serializers import AuctionItemSerializer
from channels.layers import get_channel_layer
from asgiref.sync import async_to_sync
import decimal 

class AuctionItemListView(ListAPIView):
    queryset = AuctionItem.objects.filter(ends_at__gt=timezone.now())
    serializer_class = AuctionItemSerializer

class PlaceBidView(APIView):
   
    def post(self, request, item_id):
        try:
            amount = decimal.Decimal(request.data.get('amount'))
        except (decimal.InvalidOperation, TypeError, ValueError):
            return Response({'error': 'Invalid bid amount provided.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            
            with transaction.atomic():

                item = AuctionItem.objects.select_for_update().get(pk=item_id)

                if not item.is_active: 
                    return Response({'error': 'This auction has ended.'}, status=status.HTTP_400_BAD_REQUEST)

                if amount <= item.current_price:
                    return Response(
                        {'error': f'Bid must be higher than the current price ({item.current_price}).'}, 
                        status=status.HTTP_400_BAD_REQUEST
                    )


                item.current_price = amount
                item.save()

            channel_layer = get_channel_layer() 
            room_group = f'auction_{item.id}'

            async_to_sync(channel_layer.group_send)(
                room_group,
                {
                    'type': 'broadcast_price', 
                    'price': str(item.current_price) 
                }
            )

            
            serializer = AuctionItemSerializer(item)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except AuctionItem.DoesNotExist:
            return Response({'error': 'Auction item not found.'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)