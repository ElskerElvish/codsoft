from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length= 100)
    price = models.IntegerField()
    descprice = models.CharField(max_length=255, blank=True, null=True)
    image = models.ImageField(upload_to = "uploads/showroom", blank=True, null=True)

    def __str__(self):
        return self.name
    
    @staticmethod
    def get_all():
        return Product.objects.all()
    
    @staticmethod
    def get_by_id(id):
        return Product.objects.get(id=id)


class Order(models.Model):
    order_id = models.CharField(max_length=100)
    order_date = models.DateTimeField(auto_now_add=True)

    phone = models.CharField(max_length=15, blank=True, null=True)
    address = models.CharField(max_length=500, default='')
    
    order_amount = models.IntegerField()
    order_products = models.CharField(max_length=200, default='')

    order_user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    payment_status = models.CharField(max_length=100, default='not-initialized')
    razorpay_payment_id = models.CharField(max_length=500)
    razorpay_order_id = models.CharField(max_length=500)
    razorpay_signature = models.CharField(max_length=600)  #del iit

    
    def __str__(self):
        return self.order_id
    
    @staticmethod
    def GetByOrderId(oid):
        return Order.objects.get(order_id=oid)
    
    @staticmethod
    def get_by_user(username):
        return Order.objects.filter(order_user=username)


