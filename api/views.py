from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, IsAdminUser, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from api.serializers import (
    UserSerializer,
    ProductSerializer,
    UserRegisterationSerializer,
    ProductWishListSerializer,
)
from users.models import User, Product


class RegisterUser(generics.CreateAPIView):
    serializer_class = UserRegisterationSerializer
    queryset = User.objects.all()
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        tokens = self.get_tokens_for_user(user=user)
        data = {**serializer.data, "token": tokens}
        return Response(data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }
        return tokens


class ListUsers(generics.ListAPIView):
    permission_classes = [IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ListProducts(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class ViewProduct(generics.RetrieveUpdateAPIView):
    serializer_class = ProductWishListSerializer
    lookup_field = "name"

    def get_queryset(self):
        pk = self.kwargs["name"]
        return Product.objects.filter(name=pk)

    def perform_update(self, serializer):
        serializer.save(wishlist=[self.request.user])


class ListCreateProduct(generics.ListCreateAPIView):
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Product.objects.filter(seller=self.request.user)

    def perform_create(self, serializer):
        serializer.save(seller=self.request.user)


class ListWishList(generics.ListAPIView):
    serializer_class = ProductSerializer

    def get_queryset(self):
        return self.request.user.wishlist.all()
