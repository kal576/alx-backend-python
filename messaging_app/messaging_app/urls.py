from django.urls import path, include
from rest_framework_simplejwt.views import(
    TokenObtainPairView,
    TokenRefreshView,
)

urlpatterns = [
    path('api-auth/', include('chats.urls')),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair_view'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh_view')
]
