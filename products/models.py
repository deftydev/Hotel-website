import datetime
from django.db import models
from django.conf import settings

from django.contrib.auth.models import User

LEVELS=(
    ('Single','Single'),
    ('Double','Double'),
    ('Quad','Quad'),
    ('King','King')
)


class Product(models.Model):
    roomtype    =models.CharField(max_length=40,choices=LEVELS)
    description =models.CharField(max_length=240)
    image       =models.ImageField(upload_to='images/',blank=True)
    votes_total =models.IntegerField(default=1 )
    price       =models.IntegerField()


    def __str__(self):
        return self.roomtype

    class Meta:
        ordering=['-id']


class Available(models.Model):
    product         = models.ForeignKey(Product, on_delete=models.CASCADE)
    rooms_available = models.IntegerField()
    date            = models.DateTimeField(auto_now_add=True)


class Order(models.Model):
    user     = models.ForeignKey(settings.AUTH_USER_MODEL,on_delete=models.CASCADE)
    ordered  = models.BooleanField(default=True)
    product  = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity} of {self.product.roomtype}"

    def save(self, *args, **kwargs):
        super(Order, self).save(*args, **kwargs)
        last_available = Available.objects.filter(product=self.product).latest('date')
        Available.objects.create(date=datetime.datetime.now(),product=self.product, rooms_available=last_available.rooms_available - self.quantity)

    def get_final_price(self):
         return self.quantity * self.product.price

#
#
# class Order(models.Model):
#     user = models.ForeignKey(settings.AUTH_USER_MODEL,
#                              on_delete=models.CASCADE)
#     ref_code = models.CharField(max_length=20, blank=True, null=True)
#     products = models.ManyToManyField(OrderItem)
#     ordered_date = models.DateTimeField()
#     ordered = models.BooleanField(default=False)
#     contact=models.IntegerField()
#
#
#
#     def __str__(self):
#         return self.user.username
#
#     def get_total(self):
#         total = 0
#         for order_item in self.products.all():
#             total += order_item.get_final_price()
#         if self.coupon:
#             total -= self.coupon.amount
        # return total
