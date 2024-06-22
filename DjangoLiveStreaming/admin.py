# DjangoLiveStreaming/admin.py
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Donation, Stream, Comment

# Register the User model with UserAdmin
admin.site.register(User, UserAdmin)

# Create a custom admin class for the Donation model
class DonationAdmin(admin.ModelAdmin):
    list_display = ('id', 'amount', 'message', 'stream', 'donor', 'payment_method', 'status', 'transaction_id', 'created_at', 'updated_at')
    search_fields = ('transaction_id', 'donor__username', 'stream__title')
    list_filter = ('status', 'payment_method', 'created_at', 'updated_at')

# Register the Donation model with the custom admin class
admin.site.register(Donation, DonationAdmin)

# Create a custom admin class for the Stream model
class StreamAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'description', 'streamer', 'is_active', 'created_at', 'updated_at')
    search_fields = ('title', 'description', 'streamer__username')
    list_filter = ('is_active', 'created_at', 'updated_at')

# Register the Stream model with the custom admin class
admin.site.register(Stream, StreamAdmin)


# Create a custom admin class for the Comment model
class CommentAdmin(admin.ModelAdmin):
    list_display = ('id', 'content', 'stream', 'user', 'created_at', 'updated_at')
    search_fields = ('content', 'user__username', 'stream__title')
    list_filter = ('created_at', 'updated_at')

# Register the Comment model with the custom admin class
admin.site.register(Comment, CommentAdmin)