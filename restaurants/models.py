from django.contrib.auth.models import AbstractUser
from django.db import models
from django_enum import EnumField

# Create your models here.


class RestaurantDocumentsEnum(models.TextChoices):
    PAN = "PAN"
    GST = "GST"
    FSSAI = "FSSAI"


class UserType(models.TextChoices):
    MANAGER = "MANAGER"
    CUSTOMER = "CUSTOMER"
    ADMIN = "ADMIN"
    OWNER = "OWNER"
    RIDER = "RIDER"


class RestaurantStatus(models.TextChoices):
    PENDING = "PENDING"
    IN_REVIEW = "IN_REVIEW"
    DECLINED = "DECLINED"
    APPROVED = "APPROVED"


class FoodType(models.TextChoices):
    VEGETARIAN = "VEGETARIAN"
    NON_VEGETARIAN = "NON_VEGETARIAN"
    BOTH = "BOTH"


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    deleted_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(
        "CustomUser", on_delete=models.DO_NOTHING, null=True, blank=True
    )
    updated_by = models.ForeignKey(
        "CustomUser", on_delete=models.DO_NOTHING, null=True, blank=True
    )
    deleted_by = models.ForeignKey(
        "CustomUser", on_delete=models.DO_NOTHING, null=True, blank=True
    )
    is_acitve = models.BooleanField(default=False)

    class Meta:
        abstract = True


class CustomUser(BaseModel, AbstractUser):
    """
    This model represents Users of app.

    Attributes:

    first_name(CharField): The first name of user
    last_name(charField): Last name of user
    email(EmailField): Email of user
    contact_number(IntegerField): Mobile number of user
    type(Enum): User type like Customer, restaurant owner ,admin or rider(driver)

    """

    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.IntegerField()
    type = EnumField(UserType, default="CUSTOMER")

    def __str__(self):
        return self.first_name + " " + self.last_name

    class Meta:
        db_table = "user"


class Location(BaseModel):
    """
    This model represents location of the restaurant

    Attributes:

    address(CharField): Proper/exact address like flat number,society name,floor , Office number etc.
    restaurant(ForeignKey): Represent restaurant id
    latitude(FloatField): Used to fetch location
    longitude(FloatField): Used to fetch location

    """

    address = models.CharField(max_length=255)
    restaurant = models.ForeignKey("Restaurant", on_delete=models.CASCADE)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.restaurant.restaurant_name

    class Meta:
        db_table = "restaurant_location"


class Restaurant(BaseModel):
    """
    This model is used to add restaurant

    Attributes:

    restaurant_name(CharField): name of the restaurant
    restaurant_phone(IntegerField): contact number of restaurant
    invoicing_email(EmailField): A kind of business email.Will receive business related email notifications.
    is_open(BooleanField) : Set to true when restaurant is open
    owner_name(CharField): Name of the restaurant owner
    owner_email(EmailField): Email address of restaurant owner
    license_registration_image(FileField): FSSAI license image
    license_registration_number(IntegerField): FSSAI license number
    license_expiration_date(DateField): FSSAI license expire date
    bank_account_image(FileField): Image of bank passbook / cancel cheque
    bank_account_number(CharField): Bank account number
    bank_ifsc_code(CharField): Bank IFSC code
    parent_restaurant(ForeignKey): self referencing foreign key to ensure about restaurant's multiple branches.
    location(ForeignKey): Location of restaurant
    manager(ForeignKey): Manager will be added in CustomUser model as a type = 'manager' after restaurant request will approved.

    """

    restaurant_name = models.CharField(max_length=255)
    restaurant_phone = models.IntegerField()
    invoicing_email = models.EmailField()
    is_open = models.BooleanField(default=False)
    owner_name = models.CharField(max_length=255)
    owner_email = models.EmailField()

    license_registration_image = models.FileField()
    license_registration_number = models.IntegerField()
    license_expiration_date = models.DateField()

    bank_account_image = models.FileField()
    bank_account_number = models.CharField(max_length=255)
    bank_ifsc_code = models.CharField(max_length=11)

    parent_restaurant = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="branches",
    )
    location = models.ForeignKey(
        Location,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="location",
    )
    manager = models.ForeignKey(
        CustomUser, on_delete=models.SET_NULL, null=True, blank=True
    )

    def __str__(self):
        return self.restaurant_name

    class Meta:
        db_table = "restaurants_restaurant"


class RestaurantDocument(BaseModel):
    """
    This model represents restaurant documents.

    Attributes:

    restaurant(ForeignKey): Represents restaurant id
    document_type(Enum): Type of document
    document_number(CharField): Document number
    document_image(FileFIeld): Image of document
    """

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    document_type = EnumField(RestaurantDocumentsEnum)
    document_number = models.CharField(max_length=255)

    document_image = models.FileField(upload_to="Documents/")

    def __str__(self):
        return self.document_type

    class Meta:
        db_table = "restaurants_document"


class RestaurantRequest(BaseModel):
    """
    This model represents restaurant request status and reason

    Attributes:

    restaurant(ForeignKey): Restaurant id
    approval_status(Enum): Status of restaurant request like pending, approved, in_review or declined.
    reason(TextField): Reason if admin decline the request
    """

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    approval_status = EnumField(RestaurantStatus, default="PENDING")
    reason = models.TextField()

    def __str__(self):
        return self.restaurant.restaurant_name

    class Meta:
        db_table = "restaurants_request"


class MenuImage(BaseModel):
    """
    This model represents Images for menu of restaurant

    Attributes:

    image(FileField): Upload multiple images for the menu
    """

    image = models.FileField(upload_to="Documents/")

    class Meta:
        db_table = "restaurants_menuimage"


class RestaurantMenu(BaseModel):
    """
    This model represents restaurant's menu

    Attributes:

    restaurant(ForeignKey): Restaurant id
    type_of_cuisine(CharField): Cuisines like chinese,indian etc.
    type_of_food(Enum): Food available in restaurant like veg or non veg
    image(ManyToManyField): Images of the restaurant menu

    """

    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE)
    type_of_cuisine = models.CharField(max_length=255)
    type_of_food = EnumField(FoodType)
    image = models.ManyToManyField(MenuImage)

    def __str__(self):
        return self.restaurant.restaurant_name

    class Meta:
        db_table = "restaurant_menu"
