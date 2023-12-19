from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from phonenumber_field.modelfields import PhoneNumberField

# Create your models here.


def upload_image_path(filename, instance):
    if instance.document_type:
        upload_path = f"restaurant/documents/{instance.document_type}/{filename}"
    elif instance.bank_account_image:
        upload_path = f"restaurant/documents/Bank/{filename}"
    else:
        upload_path = f"restaurant/documents/License/{filename}"
    return upload_path


class UserManager(BaseUserManager):
    def create_user(self, validated_data):
        """Create a user."""

        if not validated_data.get("email"):
            raise ValueError("Users must have an email address")

        user = self.model(
            email=self.normalize_email(validated_data.get("email", "")),
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name", ""),
            contact_number=validated_data.get("contact_number", ""),
            profile_pic=validated_data.get("profile_pic", ""),
        )
        user.save()
        return user

    def create_superuser(self, email, password):
        """Create a superuser."""

        super_user_obj = {}
        super_user_obj["email"] = email
        super_user_obj["password"] = password
        super_user_obj["first_name"] = "Admin"
        user = self.create_user(super_user_obj)
        user.save()
        return user


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True)
    deleted_at = models.DateTimeField(null=True, blank=True)
    created_by = models.ForeignKey(
        "CustomUser",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="%(class)s_created_by",
    )
    updated_by = models.ForeignKey(
        "CustomUser",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="%(class)s_updates_by",
    )
    deleted_by = models.ForeignKey(
        "CustomUser",
        on_delete=models.DO_NOTHING,
        null=True,
        blank=True,
        related_name="%(class)s_deleted_by",
    )
    is_active = models.BooleanField(default=False)

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
    profile_image(File): Profile pic of user
    """

    TYPES = (
        ("MANAGER", "MANAGER"),
        ("CUSTOMER", "CUSTOMER"),
        ("ADMIN", "ADMIN"),
        ("OWNER", "OWNER"),
        ("RIDER", "RIDER"),
    )
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255, null=True, blank=True)
    email = models.EmailField(unique=True)
    contact_number = PhoneNumberField(null=True, blank=True)
    type = models.CharField(max_length=255, choices=TYPES, default="CUSTOMER")
    profile_image = models.ImageField(
        null=True,
        blank=True,
        upload_to=lambda instance, filename: f"users/{instance.type}/_{filename}",
    )
    email_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(
        default=False, help_text="Designates that this user has all permissions"
    )
    objects = UserManager()

    USERNAME_FIELD = "email"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    class Meta:
        db_table = "users"


class Location(BaseModel):
    """
    This model represents location of the restaurant

    Attributes:

    address(CharField): Proper/exact address like flat number,society name,floor , Office number etc.
    latitude(FloatField): Used to fetch location
    longitude(FloatField): Used to fetch location

    """

    address = models.CharField(max_length=255)
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return self.address

    class Meta:
        db_table = "restaurant_locations"


class Image(models.Model):
    """
    This model represents Images for menu or bank images of restaurant

    Attributes:

    image(FileField): Upload multiple images for the menu or bank account images
    """

    image = models.FileField(upload_to=upload_image_path)


class RestaurantOutlet(BaseModel):
    """
    This model represents restaurant outlet like roadside cafe , diner ,  grill or riverside cafe etc.

    Attributes:

    outlet_name(CharField): Outlet of the restaurant like roadside cafe , diner , riverside cafe etc.
    """

    outlet_name = models.CharField(max_length=255)

    def __str__(self):
        return self.outlet_name

    class Meta:
        db_table = "restaurant_outlets"


class Restaurant(BaseModel):
    """
    This model is used to add restaurant

    Attributes:

    name(CharField): name of the restaurant
    phone(IntegerField): contact number of restaurant
    outlet(Foreignkey): the outlet of the restaurant (means type like cafe or diner etc.)
    cuisine(CharField): Cuisines of restaurants like Indian , Chinese , Panjabi etc.
    type_of_food(CharField): Food type like vegetarian , non-vegetarian or both.
    menu_image(ManyToManyField): Multiple images of restaurant menu
    invoicing_email(EmailField): A kind of business email.Will receive business related email notifications.
    is_open(BooleanField) : Set to true when restaurant is open
    owner_name(CharField): Name of the restaurant owner
    owner_email(EmailField): Email address of restaurant owner
    license_image(FileField): FSSAI license image
    license_registration_number(IntegerField): FSSAI license number
    license_expiration_date(DateField): FSSAI license expire date
    bank_account_image(ManyToManyField): Image of bank passbook / cancel cheque
    bank_account_number(CharField): Bank account number
    bank_ifsc_code(CharField): Bank IFSC code
    parent_restaurant(ForeignKey): self referencing foreign key to ensure about restaurant's multiple branches.
    location(ForeignKey): Location of restaurant
    manager(ForeignKey): Manager will be added in CustomUser model as a type = 'manager' after restaurant request will approved.

    """

    FOOD_TYPES = (
        ("VEGETARIAN", "VEGETARIAN"),
        ("NON_VEGETARIAN", "NON_VEGETARIAN"),
        ("BOTH", "BOTH"),
    )
    name = models.CharField(max_length=255)
    contact_number = PhoneNumberField()
    outlet = models.ForeignKey(
        RestaurantOutlet,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="restaurants",
    )
    cuisine = models.CharField(max_length=255)
    type_of_food = models.CharField(max_length=255, choices=FOOD_TYPES)
    menu_image = models.ManyToManyField(Image)
    invoicing_email = models.EmailField()
    is_open = models.BooleanField(default=False)
    owner_name = models.CharField(max_length=255)
    owner_email = models.EmailField()

    license_image = models.FileField(upload_to=upload_image_path)
    license_registration_number = models.IntegerField()
    license_expiration_date = models.DateField()

    bank_account_image = models.ManyToManyField(Image)
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
        related_name="restaurants",
    )
    manager = models.ForeignKey(
        CustomUser,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="restaurants",
    )

    def __str__(self):
        return self.name

    class Meta:
        db_table = "restaurants"


class RestaurantDocument(BaseModel):
    """
    This model represents restaurant documents.

    Attributes:

    restaurant(ForeignKey): Represents restaurant id
    document_type(Enum): Type of document
    document_number(CharField): Document number
    document_image(FileFIeld): Image of document
    """

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="restaurant_documents"
    )
    document_type = models.CharField(
        max_length=255, help_text="type of documents as GST,PAN etc."
    )
    document_number = models.CharField(max_length=255)

    document_image = models.FileField(upload_to=upload_image_path)

    def __str__(self):
        return self.document_type

    class Meta:
        db_table = "restaurant_documents"


class RestaurantStatusEnum(models.TextChoices):
    APPROVED = "APPROVED", "APPROVED"
    PENDING = "PENDING", "PENDING"
    IN_REVIEW = "IN_REVIEW", "IN_REVIEW"
    DECLINED = "DECLINED", "DECLINED"


class RestaurantRequest(BaseModel):
    """
    This model represents restaurant request status and reason

    Attributes:

    restaurant(ForeignKey): Restaurant id
    approval_status(Enum): Status of restaurant request like pending, approved, in_review or declined.
    reason(TextField): Reason if admin decline the request
    """

    restaurant = models.ForeignKey(
        Restaurant, on_delete=models.CASCADE, related_name="restaurant_requests"
    )
    status = models.CharField(
        max_length=255, choices=RestaurantStatusEnum.choices, default="PENDING"
    )
    reason = models.TextField()

    def __str__(self):
        return self.restaurant.name

    class Meta:
        db_table = "restaurant_requests"
