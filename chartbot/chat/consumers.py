import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from api.services import InfermedicaService
from api.models import Conversation, Message

class ChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        await self.accept()
        self.conversation = await self.create_conversation()
        
    async def disconnect(self, close_code):
        await self.close_conversation()
        
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message = text_data_json['message']
        
        # Save user message
        await self.save_message(message, is_bot=False)
        
        # Process message and get response
        response = await self.process_message(message)
        
        # Save bot response
        await self.save_message(response, is_bot=True)
        
        await self.send(text_data=json.dumps({
            'message': response
        }))
    
    @database_sync_to_async
    def create_conversation(self):
        return Conversation.objects.create(user=self.scope['user'])
    
    @database_sync_to_async
    def close_conversation(self):
        if hasattr(self, 'conversation'):
            self.conversation.ended_at = timezone.now()
            self.conversation.save()
    
    @database_sync_to_async
    def save_message(self, content, is_bot):
        return Message.objects.create(
            conversation=self.conversation,
            content=content,
            is_bot=is_bot
        )
    
    async def process_message(self, message):
        # Here you would integrate with InfermedicaService
        # This is a placeholder response
        return f"I understand you said: {message}. How can I help you further?"