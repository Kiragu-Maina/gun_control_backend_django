"""conrates URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from .views import RegisterView, LoginView, ProductsView, ProductsUpload, CheckShop, CreateShop, CategoriesView, HandleReturnView


urlpatterns = [
   
    
    path('register/', RegisterView.as_view(), name='api-register'),
    path('login/', LoginView.as_view(), name='api-login'),
    path('products/<str:username>/<int:product_id>/', ProductsUpload.as_view(), name='uploadproducts'),
    path('ecommerce/<str:username>/', ProductsView.as_view(), name='ecommerce'),
    path('checkshop/<str:username>/', CheckShop.as_view(), name='checkshop'),
    path('createshop/', CreateShop.as_view(), name='createshop'),   
    path('categories/', CategoriesView.as_view(), name='categories'),
    path('return/', HandleReturnView.as_view(), name='return')
]   