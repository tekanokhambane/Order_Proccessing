from django.contrib.auth import authenticate, login
from rest_framework.authentication import BasicAuthentication
from rest_framework.permissions import IsAuthenticated, AllowAny

# from rest_framework.views import APIView
from adrf.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator


class SessionLoginView(APIView):
    permission_classes = [AllowAny]

    async def post(self, request, *args, **kwargs):
        email = request.data.get("email")
        password = request.data.get("password")
        user = await authenticate(request, email=email, password=password)
        if user is not None:
            return Response(
                {"detail": "Successfully logged in."}, status=status.HTTP_200_OK
            )
        else:
            return Response(
                {"detail": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED
            )


class SessionUserView(APIView):
    permission_classes = [IsAuthenticated]

    @method_decorator(cache_page(60 * 20))
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            print(request.user)
            return Response(
                {
                    "detail": "You are already logged in.",
                    "user": {
                        "email": request.user.email,
                        "username": request.user.username,
                        "first_name": request.user.first_name,
                        "last_name": request.user.last_name,
                        "id": request.user.id,
                    },
                },
                status=status.HTTP_200_OK,
            )
        else:
            print(request.user)
            return Response(
                {"detail": "You are not logged in."},
                status=status.HTTP_401_UNAUTHORIZED,
            )
