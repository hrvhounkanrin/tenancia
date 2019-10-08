"""Customuser views."""
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from customuser.serializers import UserSerializer


class CreateUSerApiView(APIView):
    """Customuser apiview."""

    permission_classes = (AllowAny,)

    def post(self, request):
        """Create user."""
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer_context = {
            'request': request,
        }
        serializer.save()
        return Response(serializer.data,
                        context=serializer_context,
                        status=status.HTTP_201_CREATED)
