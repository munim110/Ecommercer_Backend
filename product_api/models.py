from django.db import models
from user_api.models import SiteUser

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    photo = models.ImageField(upload_to='products', null=True, blank=True)
    price = models.DecimalField(max_digits=6, decimal_places=2)
    quantity = models.IntegerField()


    def __str__(self):
        return self.name


class CartItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)

    def __str__(self):
        return self.product.name + ' - ' + str(self.quantity)

    def get_total(self):
        return self.product.price * self.quantity
    

class Cart(models.Model):
    user = models.ForeignKey(SiteUser, related_name='carts', on_delete=models.CASCADE, blank=True)
    items = models.ManyToManyField(CartItem, blank=True)

    def __str__(self):
        return str(self.user.username)

    def add_to_cart(self, product_id):
        product = Product.objects.get(id=product_id)
        
        # check if the quantity is available
        if product.quantity <= 0:
            return False

        # check if the user already has this item in the cart
        for cart_item in self.items.all():
            if cart_item.product == product:
                cart_item.quantity += 1
                cart_item.save()
                return
        new_item, _ = CartItem.objects.get_or_create(product=product, quantity=1)
        if new_item not in self.items.all():
            self.items.add(new_item)
            self.save()

    def remove_from_cart(self, product_id):
        product = Product.objects.get(id=product_id)
        for cart_item in self.items.all():
            if cart_item.product == product:
                self.items.remove(cart_item)
                cart_item.delete()
                self.save()
                break

    def change_quantity(self, product_id, quantity):
        product = Product.objects.get(id=product_id)
        for cart_item in self.items.all():
            if cart_item.product == product:
                cart_item.quantity = quantity
                cart_item.save()
                break

    def get_cart_items(self):
        return self.items.all()

    def get_cart_total(self):
        total = 0
        for cart_item in self.items.all():
            total += cart_item.get_total()
        return total

    def clear(self):
        for item in self.items.all():
            item.delete()
        self.save()

    def checkout(self):
        for cart_item in self.items.all():
            product = cart_item.product
            product.quantity -= cart_item.quantity
            product.save()
        self.clear()

