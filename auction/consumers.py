
import json
from channels.generic.websocket import AsyncWebsocketConsumer

class AuctionConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.item_id = self.scope['url_route']['kwargs']['item_id']
        self.room_group_name = f'auction_{self.item_id}'

        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()
        print(f"WebSocket connected for item {self.item_id}") 

    async def disconnect(self, close_code):

        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )
        print(f"WebSocket disconnected for item {self.item_id}") 

    async def broadcast_price(self, event):
        new_price = event['price']

        await self.send(text_data=json.dumps({
            'new_price': new_price
        }))
        print(f"Broadcasting new price {new_price} for item {self.item_id}") 
