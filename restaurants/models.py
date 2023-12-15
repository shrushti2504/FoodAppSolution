from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Restaurant(BaseModel):
    restaurant_name = models.CharField(max_length=255)
    address = models.TextField()
    latitude = models.FloatField()  # for location
    longitude = models.FloatField()  # for location
    restaurant_contact_number = models.IntegerField()

    manager_name = models.CharField(max_length=255)
    manager_contact_number = models.IntegerField()
    manager_email = models.EmailField()
    owner_name = models.CharField(max_length=255)
    owner_contact_number = models.IntegerField()
    owner_email = models.EmailField()

    pan_card = models.FileField()
    pan_cart_number = models.CharField(max_length=10)

    fssai_license = models.FileField()
    fssai_license_number = models.IntegerField()
    fssai_expiration_date = models.DateField()

    gst_certificate = models.FileField()
    gst_number = models.CharField(max_length=15)

    bank_passbook = models.FileField()
    bank_account_number = models.CharField(max_length=255)
    bank_ifsc_code = models.CharField(max_length=11)

    cuisines = models.CharField(max_length=255)
    menu = models.ImageField()

    is_approved = models.BooleanField(default=False)
    # when admin set this field as true then restaurant will be live for customers. Till then it will be consider restaurant as a requested restaurant.

    def __str__(self):
        return self.restaurant_name
