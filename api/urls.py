from django.urls import path
from livechat.views import CreateAccountAPIView, LoginApiView , ChatAPIView
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)


urlpatterns = [
    path('createacc/', CreateAccountAPIView.as_view(), name='create_account_api'),
    path('login/', LoginApiView.as_view(), name='login_api'),
    path('chat/', ChatAPIView.as_view(), name='chat_api'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
