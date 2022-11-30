from rest_framework import serializers
from product_api.models import *

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id','name', 'description', 'price', 'quantity', 'photo']
        extra_kwargs = {'photo': {'required': False}}
        depth = 1

    def create(self, validated_data):
        return Product.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.name = validated_data.get('name', instance.name)
        instance.description = validated_data.get('description', instance.description)
        instance.price = validated_data.get('price', instance.price)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.photo = validated_data.get('photo', instance.photo)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return instance


class CartItemSerializer(serializers.ModelSerializer):
    product = serializers.PrimaryKeyRelatedField(queryset=Product.objects.all())
    class Meta:
        model = CartItem
        fields = ['product', 'quantity']
        depth = 1

    def create(self, validated_data):
        return CartItem.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.product = validated_data.get('product', instance.product)
        instance.quantity = validated_data.get('quantity', instance.quantity)
        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return instance


class CartSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=SiteUser.objects.all())
    items = CartItemSerializer(many=True)
    class Meta:
        model = Cart
        fields = ['user' ,'items']
        depth = 1

    def create(self, validated_data):
        return Cart.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        items = validated_data.pop('items')
        instance.user = validated_data.get('user', instance.user)
        for item in items:
            if item.get('id'):
                CartItem.objects.filter(id=item['id']).update(**item)
            else:
                new_item = CartItem.objects.create(product=item['product'], quantity=item['quantity'])
                instance.items.add(new_item)

        instance.save()
        return instance

    def delete(self, instance):
        instance.delete()
        return instance


class OrderSerializer(serializers.ModelSerializer):
    user = serializers.PrimaryKeyRelatedField(queryset=SiteUser.objects.all())
    items = CartItemSerializer(many=True)
    class Meta:
        model = Order
        fields = ['id', 'user', 'items', 'status', 'date', 'address']
        depth = 1

    def create(self, validated_data):
        user = validated_data.get('user')
        items = validated_data.get('items')
        address = validated_data.get('address')
        order = Order.objects.create(user=user, address=address)
        for item in items:
            new_item = CartItem.objects.create(product=item['product'], quantity=item['quantity'])
            order.items.add(new_item)

        order.save()
        return order
    
    def update(self, instance, validated_data):
        instance.status = validated_data.get('status', instance.status)
        instance.save()
        return instance