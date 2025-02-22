from django.utils.timezone import now
from django_q.tasks import schedule
from django.core.mail import send_mail
from fleet_manager.models import Asset
from datetime import timedelta


def send_vehicle_expiry_reminder():
    # Get assets expiring in 7 days
    expiring_assets = Asset.objects.filter(
        purchasedetails__disc_expiry_date__isnull=False,
        purchasedetails__disc_expiry_date__lte=now() + timedelta(days=30),
    )

    for asset in expiring_assets:
        send_mail(
            subject="Vehicle Expiry Reminder",
            message=f"Your vehicle {asset.make} {asset.model} (VIN: {asset.vin}) is expiring soon.",
            from_email="admin@lingode.co.za",
            recipient_list=["info@lingode.co.za"],
            fail_silently=False,
        )


# Schedule the function to run daily
schedule(
    "fleet_manager.tasks.send_vehicle_expiry_reminder",
    schedule_type="D",  # Run Daily
    # next_run=now() + timedelta(minutes=1),  # First run in 1 minute for testing
)
