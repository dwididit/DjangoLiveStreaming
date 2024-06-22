from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'streams', views.StreamViewSet)
router.register(r'donations', views.DonationViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', views.register_user, name='register_user'),
    path('api/login/', views.login_user, name='login_user'),
    path('api/logout/', views.logout_user, name='logout_user'),
    path('api/donations/create/', views.DonationViewSet.as_view({'post': 'create'}), name='create_donation'),
    path('api/donations/<int:pk>/confirm/', views.DonationViewSet.as_view({'post': 'confirm'}), name='confirm_donation'),
    path('api/donations/', views.DonationViewSet.as_view({'get': 'list'}), name='stream_donations'),
    path('api/comments/create/', views.CommentViewSet.as_view({'post': 'create'}), name='create_comment'),
    path('api/comments/<int:pk>/', views.CommentViewSet.as_view({'get': 'retrieve'}), name='stream_comments'),
    path('api/', include(router.urls)),
]