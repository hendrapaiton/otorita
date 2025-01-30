from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, permission_classes
from django.views.generic import TemplateView


class CustomTokenObtainPairView(TokenObtainPairView):
    def post(self, request, *args, **kwargs):
        response = super().post(request, *args, **kwargs)

        if response.status_code == 200:
            refresh_token = response.data.pop('refresh', None)
            if refresh_token:
                response.set_cookie(
                    key='token',
                    value=refresh_token,
                    httponly=True,
                    secure=True,
                    samesite='Lax',
                    max_age=60 * 60 * 24 * 7,
                    path='/api/token/refresh/'
                )

        return response


class CustomTokenRefreshView(TokenRefreshView):
    def post(self, request, *args, **kwargs):
        refresh_token = request.COOKIES.get('token')

        if not refresh_token:
            return Response(
                {'detail': 'Refresh token tidak ditemukan'},
                status=status.HTTP_401_UNAUTHORIZED
            )

        request.data['refresh'] = refresh_token
        return super().post(request, *args, **kwargs)


class LogoutView(APIView):
    def post(self, request):
        response = Response({'detail': 'Logout berhasil'})
        response.delete_cookie('token')

        refresh_token = request.COOKIES.get('token')
        if refresh_token:
            try:
                token = RefreshToken(refresh_token)
                token.blacklist()
            except Exception as e:
                pass

        return response


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def protected_page(request):
    return Response({'detail': 'This is a protected page'}, status=status.HTTP_200_OK)


class IndexApi(APIView):
    def get(self, request, *args, **kwargs):
        return Response(
            {'message': 'Selamat datang di Nusantara'},
            status=status.HTTP_200_OK
        )


class IndexView(TemplateView):
    template_name = 'index.html'
