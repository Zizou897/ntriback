
from django.urls import path, include

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from .routers import router
from .viewset import ContactViewSet
from .views import PasswordResetRequestView, PasswordResetConfirmView, NotificationListAPIView, MarquerCommeLueAPIView, CustomLoginView



urlpatterns = [
    path('v1/', include(router.urls)),
    path('v1/contacts/', ContactViewSet.as_view(), name='api-contact'),
    
    path('v1/token/', CustomLoginView.as_view(), name='token_obtain_pair'),
    path('v1/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    
    path('v1/password-reset/', PasswordResetRequestView.as_view(), name="password-reset"),
    path('v1/password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(), name="password-reset-confirm"),
    
    path('v1/notifications/', NotificationListAPIView.as_view(), name='notification-liste'),
    path('v1/notifications/lue/<int:notif_id>/', MarquerCommeLueAPIView.as_view(), name='notification-lue'),
    
]