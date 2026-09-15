from django.db import models

# Create your models here.


class Registration(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    date_of_birth = models.DateField(null=True, blank=True)

class Bill(models.Model):

    customer_id = models.ForeignKey(
        'Registration',
        on_delete=models.CASCADE
    )

    bill_id = models.CharField(
        max_length=100,
        unique=True
    )

    bill_code = models.CharField(
        max_length=100,
        unique=True,
        default=0
    )
    bill_status = models.CharField(
        max_length=100,
        default="yes"
    )


    bill_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2
    )

    bill_picture = models.ImageField(
        upload_to='bills/'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

