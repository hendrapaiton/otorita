from django.urls import path
from .views import CustomTokenObtainPairView, CustomTokenRefreshView, IndexApi, LogoutView, IndexView, protected_page

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('api/', IndexApi.as_view(), name='index-api'),
    path('api/token/', CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', CustomTokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout/', LogoutView.as_view(), name='logout'),
    path('api/protected/', protected_page, name='protected-page'),
]
