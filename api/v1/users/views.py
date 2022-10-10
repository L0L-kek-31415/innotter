from rest_framework.viewsets import ModelViewSet, GenericViewSet
from rest_framework import generics, mixins
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from django_filters.rest_framework import DjangoFilterBackend

from user.models import User
from api.v1.users.serializers import UserSerializer, RegisterSerializer


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        return Response(
            {
                "user": serializer.data,
                "message": "User Created Successfully. Now perform Login to get your token",
            }
        )


class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()


class SearchUserViewSet(GenericViewSet, mixins.ListModelMixin):
    serializer_class = UserSerializer
    permission_classes = (AllowAny,)
    queryset = User.objects.all()
    filter_backends = (DjangoFilterBackend,)
    filterset_fields = ("username", "email")
