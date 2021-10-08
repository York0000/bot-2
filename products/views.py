from django.db.models import Sum
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.views import APIView

from products.models import CategoryModel, ProductModel, OrderModel
from products.serializers import CategoryModelSerializer, ProductModelSerializer
from users.models import TelegramUserModel


class CategoryListAPIView(ListAPIView):
    serializer_class = CategoryModelSerializer
    queryset = CategoryModel.objects.all()


class ProductListAPIView(ListAPIView):
    serializer_class = ProductModelSerializer

    def get_queryset(self):
        pk = self.kwargs.get('pk')
        q = self.request.GET.get('q')
        cart = self.request.GET.get('products')

        if pk:
            return ProductModel.objects.filter(category_id=pk)
        elif q:
            return ProductModel.objects.filter(title__icontains=q)
        elif cart:
            cart = cart.strip('[]').replace('\'', '').split(',')
            return ProductModel.objects.filter(pk__in=cart)
        else:
            return ProductModel.objects.none()


class ProductRetrieveAPIView(RetrieveAPIView):
    serializer_class = ProductModelSerializer
    queryset = ProductModel.objects.all()


class OrderCreateAPIView(APIView):
    def post(self, request, *args, **kwargs):
        user_id = request.POST.get('user_id')
        user = TelegramUserModel.objects.get(tg_id=user_id)

        products = request.POST.get('products')
        products = products.strip('[]').replace('\'', '').split(',')

        products = ProductModel.objects.filter(pk__in=products)
        price = products.aggregate(Sum('price'))['price__sum']

        order = OrderModel.objects.create(
            user=user,
            price=price
        )

        order.products.set(products)
        order.save()

        return Response(data={'status': 'ok'})
