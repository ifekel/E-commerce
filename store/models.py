from django.db import models
from django.contrib.auth.models import User

# Create your models here. 
class Customer(models.Model):
    # So a user can only have one customer and a customer can only have one user
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    # User name
    name = models.CharField(max_length=200, null=True)
    # User email
    email = models.CharField(max_length=200)
    
    # Return a string value for the name
    def __str__(self):
        return self.name
    


class Product(models.Model):
    # Name of the product
    name = models.CharField(max_length=200, null=True)
    Label = models.TextField(default="Type Here")
    # Price of the product which is a float field
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # Check if the product needs shipping or not
    digital = models.BooleanField(default=False, blank=True, null=True)
    image = models.ImageField(null=True, blank=True)
    category = models.CharField(max_length=100, blank=True, null=True)
    
    def __str__(self):
        return self.name
    
    # @property
    def imageURL(self):
        try: 
            url = self.image.url
        except:
            url = "Sorry no image to see here"
        return url
            

    
class Order(models.Model):
    # The customer can have multiple orders
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True, blank=True)
    date_ordered = models.DateField(auto_now_add=True)
    # If complete is false it is an open cart so we can keep adding items to the cart
    # if its true it is a closed cart we need to create items and then to a different order
    complete = models.BooleanField(default=False, null=True, blank=True)
    transaction_id = models.CharField(max_length=200, null=True)
    
    
    def __str__(self):
        return str(self.customer)
    
    @property
    def shipping(self):
        shipping = False
        orderitems = self.orderitem_set.all()
        for i in orderitems:
            if i.product.digital == False:
                shipping = True
        return shipping
    
    @property
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total
    
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total
        
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True, blank=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True, blank=True)
    quantity = models.IntegerField(default=0,null=True, blank=True)
    date_added = models.DateField(auto_now_add=True)
    
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total
    
    
    def __str__(self):
        return str(self.order)
    

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE, null=True)
    order = models.ForeignKey(Order, on_delete=models.CASCADE, null=True)
    address = models.CharField(max_length=200, null=True)
    city = models.CharField(max_length=200, null=True)
    state = models.CharField(max_length=200, null=True)
    zipcode = models.CharField(max_length=200, null=True)
    date_added = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.address