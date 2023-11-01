from django.http import JsonResponse
from django.db.models import Avg
from django.views.decorators.csrf import csrf_exempt
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authtoken.models import Token

from rates.utils import utility
import json
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from .serializers import UserSerializer, ProductSerializer, ShopSerializer
from .models import Product, Shop
from django_eventstream import send_event

class ProductListView(APIView):
    permission_classes = [AllowAny]
    
    def get(self, request):
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        return Response(serializer.data)

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            email = serializer.validated_data['email']
            User.objects.create_user(username=username, email=email, password=password)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LoginView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            request.session['logged_in_user'] = username
            token, _ = Token.objects.get_or_create(user=user)

            # Include the token in the response data
            return Response({'token': token.key, 'message': 'Logged in successfully.'})
        
            
        return Response({'message': 'Invalid credentials.'}, status=status.HTTP_401_UNAUTHORIZED)





class CategoriesView(APIView):
    authentication_classes = []
    permission_classes = []
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get(self, request, *args, **kwargs):
        categories = [
                'AK47',
                'M3',
                'G3',
                '9mm',
                '16mm'
                
             
            ]

        
        return Response(categories)





class ProductsUpload(APIView):
    authentication_classes = []
    permission_classes = []

    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):

        data_list = request.data
        print(data_list)  # Assuming request.data is a list of dictionaries
        username = self.kwargs.get('username', None)

        # shop_name = request.session.get('shop_name')
        shop = Shop.objects.filter(shop_owner=username).first()

  # Assign the Shop object's ID to the 'shop' field
        context = {'shop_id': shop.id}  # Provide the shop_id in the context
        for data in data_list:
            serializer = ProductSerializer(data=data, context=context)

            
            print(serializer)
            if serializer.is_valid():
                serializer.save()
                send_event('test', 'message', {'text': 'hello world'})  # Create and save the product objects
                
            else:
                print(serializer.errors)
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        return Response({'message': 'Items created successfully.'}, status=status.HTTP_201_CREATED)
    
    def put(self, request, *args, **kwargs):
        print('put called')
        product_id = self.kwargs.get('product_id', None)  # Assuming you have a URL parameter for product_id
        print(product_id)
        username = self.kwargs.get('username', None)
        print(username)
        shop = Shop.objects.filter(shop_owner=username).first()

        context = {'shop_id': shop.id}
        try:
            product = Product.objects.get(id=product_id, shop=shop)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = ProductSerializer(product, data=request.data, context=context, partial=True)
        if serializer.is_valid():
            serializer.save()
            send_event('test', 'message', {'text': 'hello world'})
            return Response({'message': 'Product updated successfully.'}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, *args, **kwargs):
        product_id = self.kwargs.get('product_id', None)  # Assuming you have a URL parameter for product_id
        username = self.kwargs.get('username', None)
        shop = Shop.objects.filter(shop_owner=username).first()

        try:
            product = Product.objects.get(id=product_id, shop=shop)
        except Product.DoesNotExist:
            return Response({'message': 'Product not found.'}, status=status.HTTP_404_NOT_FOUND)

        product.delete()
        send_event('test', 'message', {'text': 'hello world'})
        return Response({'message': 'Product deleted successfully.'}, status=status.HTTP_204_NO_CONTENT)


class ProductsView(APIView):
    authentication_classes = []
    permission_classes = []
    
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    def get_queryset(self, request):
        print(request)
        username = self.kwargs.get('username', None)
        if username != 'none':

       
            shop_name = Shop.objects.filter(shop_owner=username).values_list('shopname', flat=True).first()
            request.session['shop_name'] = shop_name
            print('shopname in productsview is: ', shop_name)

            if shop_name is not None:
                # Do something with the shop_name
                print(f"The shop name in session is: {shop_name}")
                queryset = Product.objects.filter(shop__shopname=shop_name)
                print(queryset)
            else:
                # Handle the case when the shop_name is not found in the session
                queryset = Product.objects.all()
        else:
            queryset = Product.objects.all()
            print(queryset)

     
        return queryset

    def get(self, request, *args, **kwargs):
        username = self.kwargs.get('username', None)
        if username != 'none':

       
            shop_name = Shop.objects.filter(shop_owner=username).values_list('shopname', flat=True).first()
            request.session['shop_name'] = shop_name
            print('shopname in productsview is: ', shop_name)

            if shop_name is not None:
                # Do something with the shop_name
                print(f"The shop name in session is: {shop_name}")
                queryset = Product.objects.filter(shop__shopname=shop_name)
                print(queryset)
                serializer = ProductSerializer(queryset, many=True)
        
                return Response(serializer.data)
            else:
                # Handle the case when the shop_name is not found in the session
                queryset = Product.objects.all()
        else:
            queryset = Product.objects.all()
            serializer = ProductSerializer(queryset, many=True)
   
        dict_data = []
        for item in serializer.data:
            data_item = {
                'user': item['shop_name'],
                'type': item['category'],
                'taken': item['quantity'],
                'returned': item['returned']
            }
            if item['title'] == 'firearm':
                data_item['item_type'] = 'firearm'
            else:
                data_item['item_type'] = 'ammunition'
            dict_data.append(data_item)

        print(dict_data)
        return Response(dict_data)

        
        

class CreateShop(APIView):
    permission_classes = [AllowAny]
    def post(self, request):
        serializer = ShopSerializer(data=request.data)
        print(serializer)
        if serializer.is_valid():
            shop = serializer.save()  # Create and save the shop object
            # Additional logic or response handling
            return JsonResponse(serializer.data, status=200)
        else:
            errors = serializer.errors
            return JsonResponse(errors, status=400)
        

class CheckShop(APIView):
    authentication_classes = []
    permission_classes = []
    def get(self, request, *args, **kwargs):
        username = kwargs['username']  # Assuming 'username' is part of the URL path parameter
        # Handle the 'GET' request logic here
        # Example: Retrieve data or perform any necessary operations
        # You can use the 'username' to fetch the corresponding data from the database
        # Replace 'Shop.objects.get()' with the appropriate query to retrieve the shop_owner based on 'username'
        try:
            exists = Shop.objects.filter(shop_owner=username).exists()

            if exists:
                print('exists')
                try:
                    shop_name = Shop.objects.filter(shop_owner=username).values_list('shopname', flat=True).first()

                    if shop_name is not None:
                        # Do something with the shop_name
                        print(f"The shop name in session is: {shop_name}")
                        request.session['shop_name'] = shop_name
                        request.session.save()
                    else:
                        
                        # Handle the case when the shop_name is not found in the session
                        print("Shop name not found for the given username.")
                except Exception as e:
                    print(f"Error occurred during database query: {e}")
                
            return JsonResponse({'exists': exists, 'shopname':shop_name}, status=200)   
        except:
            return JsonResponse({'exists': False}, status=400)  

      


    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
       
        return super().dispatch(request, *args, **kwargs)
    

class HandleReturnView(APIView):
    authentication_classes = []
    permission_classes = []
    @csrf_exempt
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)
    
    
    def post(self, request, *args, **kwargs):
            data = request.data
            print(data)
            shopname=data.get('shopname')
            shop = Shop.objects.get(shopname=shopname)
            print(shop)
            
            product_id = data.get('productId')
            print(product_id)
            quantity_to_return = data.get('QuantityToReturn')

            try:
                product = Product.objects.get(shop=shop)
               
                product.returned = quantity_to_return
                product.save()
            except Product.DoesNotExist:
                return Response({'error': f'Product with ID {product_id} not found'}, status=status.HTTP_404_NOT_FOUND)
        
            return Response({'message': 'Items returned successfully.'}, status=status.HTTP_201_CREATED)