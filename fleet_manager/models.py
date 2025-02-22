from django.contrib.auth.models import AbstractUser
from django.db import models


def user_profile_pic_path(instance, filename):
    """Defines where user profile pictures will be saved."""
    return f'profile_pics/{instance.username}/{filename}'


class User(AbstractUser):
    profile_picture = models.ImageField(
        upload_to=user_profile_pic_path,
        blank=True,
        null=True,
        default="profile_pics/avator.png",
    )

    def __str__(self):
        return self.username

    @property
    def profile_picture_url(self):
        """Returns the URL of the profile picture or the default image."""
        if self.profile_picture:
            return self.profile_picture.url
        return "/media/profile_pics/avator.png"


class Asset(models.Model):
    year = models.IntegerField()
    make = models.CharField(max_length=100)
    model = models.CharField(max_length=100)
    vehicle_type = models.CharField(max_length=100)
    sub_category = models.CharField(max_length=100)
    classification = models.CharField(max_length=100)
    status = models.CharField(max_length=100)
    vin = models.CharField(max_length=100, unique=True)


class PurchaseDetails(models.Model):
    purchase_date = models.DateField()
    dealership = models.CharField(max_length=100)
    invoice_no = models.CharField(max_length=100)
    cost_price = models.DecimalField(
        max_digits=15, decimal_places=3, null=True, blank=True)
    asset = models.OneToOneField(Asset, on_delete=models.CASCADE)

    def __str__(self):
        return f"Purchase of {self.asset} from {self.dealership} on {self.purchase_date}"


class FinancingDetails(models.Model):
    funding_institution = models.CharField(max_length=100)
    loan_ref_number = models.CharField(max_length=100)
    loan_end_date = models.DateField()
    loan_terms = models.IntegerField()
    installments = models.DecimalField(max_digits=15, decimal_places=3)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    def __str__(self):
        return f"Financing for {self.asset} by {self.funding_institution}"


class LicensingDetails(models.Model):
    reg_no = models.CharField(max_length=100, unique=True)
    fleet_no = models.CharField(max_length=100, null=True)
    disc_fee = models.DecimalField(
        max_digits=15, decimal_places=3, null=True, blank=True)
    disc_expiry_date = models.DateField(null=True, blank=True)
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE)

    def __str__(self):
        return f"License for {self.asset} (Reg: {self.reg_no})"
