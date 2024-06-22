# DjangoLiveStreaming/urls.py
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenRefreshView

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
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', views.logout_user, name='logout_user'),
    path('api/', include(router.urls)),
]
