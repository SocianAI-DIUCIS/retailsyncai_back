# backend/api/urls.py
from django.urls import path
from django.http import JsonResponse
from .views import RegisterView, LoginView, ArticleListCreateView, ArticleDetailView
from rest_framework_simplejwt.views import TokenRefreshView
from .products import (
    ProductIndexCreateView,
    ProductIndexDeleteView,
    ProductListCreateView,
    ProductDetailView,
)

def api_root(request):
    return JsonResponse({
        "status": "ok",
        "endpoints": {
            "register": "/api/auth/register/",
            "login": "/api/auth/login/",
            "refresh": "/api/auth/token/refresh/",
            "articles": "/api/articles/",
            "products": "/api/products/"
        }
    })

urlpatterns = [
    path("", api_root, name="api_root"),  # <-- this is the new root route
    path("auth/register/", RegisterView.as_view(), name="register"),
    path("auth/login/", LoginView.as_view(), name="login"),
    path("auth/token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),

    path("articles/", ArticleListCreateView.as_view(), name="articles_list_create"),
    path("articles/<str:pk>/", ArticleDetailView.as_view(), name="article_detail"),

    path("products/index/create/", ProductIndexCreateView.as_view(), name="products_index_create"),
    path("products/index/", ProductIndexDeleteView.as_view(), name="products_index_delete"),
    path("products/", ProductListCreateView.as_view(), name="products_list_create"),
    path("products/<str:pk>/", ProductDetailView.as_view(), name="product_detail"),
]
