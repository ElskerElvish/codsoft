from django.contrib import admin
from . import models
# Register your models here.
class ProductAdmin(admin.ModelAdmin):
    list_diplay = ["name", "price"]


class OrderAdmin(admin.ModelAdmin):
    list_diplay = ["order_id"]

admin.site.register(models.Product, ProductAdmin )
admin.site.register(models.Order, OrderAdmin )
