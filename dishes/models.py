from django.db import models
from restaurants.models import Restaurant

# Create your models here.

STATUS = (
    ("Active", "Active"),
    (
        "In-Active",
        "In-Active",
    ),  # After set status as In-Active then , category or sub category or item is not visible to customers.
)

ORDER_STATUS = (("Accepted", "Accepted"), ("Not-Accepted", "Not-Accepted"))


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Category(BaseModel):
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    category_name = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS)
    description = models.CharField(max_length=255)
    image = models.ImageField()

    def __str__(self):
        return self.category_name


class SubCategory(BaseModel):
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE
    )  # veg ,non veg , jain etc.
    description = models.CharField(max_length=255)
    sub_category = models.CharField(
        max_length=255
    )  # panjabi , gujarati , south indian etc.
    status = models.CharField(max_length=255, choices=STATUS)
    image = models.ImageField

    def __str__(self):
        return self.sub_category


class Item(BaseModel):
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE)
    item = models.CharField(max_length=255)
    image = models.ImageField()
    description = models.CharField(max_length=255)
    status = models.CharField(max_length=255, choices=STATUS)
    price = models.IntegerField()

    def __str__(self):
        return self.item


class Cart(BaseModel):
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    customization = models.CharField(max_length=255)

    def __str__(self):
        return self.item.item


class Order(BaseModel):
    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE
    )  # we will get restaurant from cart.item.sub_category.category.restaurant to insure this order is related to which restaurants
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    status = models.CharField(max_length=255, choices=ORDER_STATUS)
    delivery_address = models.CharField(
        max_length=255
    )  # we will fetch address of customer while integrate customer app.

    def __str__(self):
        return self.cart.item
