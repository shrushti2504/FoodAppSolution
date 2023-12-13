from django.db import models

# Create your models here.


class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Restaurant(BaseModel):
    restaurant_name = models.CharField(max_length=255)
    owner_name = models.CharField(max_length=255)
    owner_email = models.EmailField()
    restaurant_contact_number = models.IntegerField()
    fssai_license = models.ImageField()
    license_registration_number = models.IntegerField()
    license_expire_date = models.DateField()
    manager_name = models.CharField(max_length=255)
    manager_email = models.EmailField()
    manager_contact_number = models.IntegerField()
    pan_card = models.ImageField()
    pan_card_number = models.CharField(max_length=15)
    gst_certificate = models.ImageField()
    gst_number = models.CharField(max_length=15)
    bank_passbook = models.ImageField()
    bank_account_number = models.IntegerField()
    ifsc_code = models.CharField(max_length=11)
    menu = models.ImageField()
    cuisine = models.CharField(
        max_length=255
    )  # chinese , indian , italian , french etc.
    logo = models.ImageField()

    def __str__(self):
        return self.restaurant_name
