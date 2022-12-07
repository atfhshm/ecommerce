from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import (
    ListUsers,
    ListProducts,
    ListCreateProduct,
    ListWishList,
    ViewProduct,
    RegisterUser,
)

urlpatterns = [
    path("register/", RegisterUser.as_view(), name="register"),
    path('login/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path("login/", TokenObtainPairView.as_view(), name="login"),
    path("users/", ListUsers.as_view()),
    path("products/", ListProducts.as_view()),
    path("product/<str:name>/", ViewProduct.as_view()),
    path("seller-products/", ListCreateProduct.as_view()),
    path("wishlist/", ListWishList.as_view()),
]
