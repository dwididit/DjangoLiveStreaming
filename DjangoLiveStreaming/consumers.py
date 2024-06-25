import json
import logging
from channels.generic.websocket import AsyncWebsocketConsumer
from rest_framework_simplejwt.tokens import UntypedToken
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError
from django.contrib.auth import get_user_model

User = get_user_model()
logger = logging.getLogger(__name__)

async def get_user(user_id):
    try:
        return await User.objects.aget(id=user_id)
    except User.DoesNotExist:
        return None

class StreamConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.stream_id = self.scope['url_route']['kwargs']['stream_id']
        self.group_name = f'stream_{self.stream_id}'
        self.user_authenticated = False
        await self.accept()
        logger.info(f"Connected to stream: {self.stream_id}")

    async def disconnect(self, close_code):
        if self.user_authenticated:
            await self.channel_layer.group_discard(
                self.group_name,
                self.channel_name
            )
        logger.info(f"Disconnected from stream: {self.stream_id}")

    async def receive(self, text_data):
        try:
            text_data_json = json.loads(text_data)
            message_type = text_data_json.get('type')

            if message_type == 'authenticate':
                token = text_data_json.get('token')
                if token:
                    try:
                        unt_token = UntypedToken(token)
                        user_id = unt_token["user_id"]
                        self.scope['user'] = await get_user(user_id)
                        if self.scope['user'] and self.scope['user'].is_authenticated:
                            self.user_authenticated = True
                            await self.channel_layer.group_add(
                                self.group_name,
                                self.channel_name
                            )
                            await self.send(text_data=json.dumps({'type': 'authentication_success'}))
                        else:
                            await self.send(text_data=json.dumps({'type': 'authentication_failure'}))
                            await self.close(code=403)
                    except (InvalidToken, TokenError) as e:
                        await self.send(text_data=json.dumps({'type': 'authentication_failure'}))
                        await self.close(code=403)
                else:
                    await self.send(text_data=json.dumps({'type': 'authentication_failure'}))
                    await self.close(code=403)
            elif self.user_authenticated:
                message = text_data_json['message']
                await self.channel_layer.group_send(
                    self.group_name,
                    {
                        'type': 'stream_message',
                        'message': message
                    }
                )
        except json.JSONDecodeError:
            pass

    async def stream_message(self, event):
        message = event['message']
        await self.send(text_data=json.dumps({
            'message': message
        }))
        logger.info(f"Message sent to WebSocket: {message}")
