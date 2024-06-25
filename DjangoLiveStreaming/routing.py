from django.urls import path
from DjangoLiveStreaming import consumers

websocket_urlpatterns = [
    path('ws/stream/<int:stream_id>/', consumers.StreamConsumer.as_asgi()),
]
