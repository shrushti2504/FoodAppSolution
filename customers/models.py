from django.db import models


# Create your models here.
class BaseModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class CustomUser(BaseModel):
    name = models.CharField(max_length=255)
    email = models.EmailField()
    contact_number = models.IntegerField()

    def __str__(self):
        return self.name
