from django.utils.timezone import now
from django_q.tasks import schedule
from django.core.mail import send_mail
from fleet_manager.models import Asset, LicensingDetails
from datetime import timedelta


def send_vehicle_expiry_reminder():
    # Get assets with licensing details expiring in 30 days
    expiring_licenses = LicensingDetails.objects.filter(
        disc_expiry_date__isnull=False,
        disc_expiry_date__lte=now() + timedelta(days=30),
    ).select_related("asset")  # Preload asset data to optimize queries

    for license_detail in expiring_licenses:
        asset = license_detail.asset  # Get related asset
        expiry_date = license_detail.disc_expiry_date.strftime("%Y-%m-%d")  # Format date

        send_mail(
            subject=f"Vehicle Expiry Reminder - {asset.vin}",
            message=(f"""
            Vehicle Expiry Reminder

            Your vehicle {asset.make} {asset.model} (VIN: {asset.vin})  
            has a license disc expiring on {expiry_date}.  

            Please ensure it is renewed before the deadline.

            Regards,  
            Fleet Management Team
            """
            ),
            from_email="admin@lingode.co.za",
            recipient_list=["info@lingode.co.za"],
            fail_silently=False,
        )


# Schedule the function to run daily
schedule(
    "fleet_manager.tasks.send_vehicle_expiry_reminder",
    schedule_type="D",  # Run Daily
    repeats=-1,  # Repeat indefinitely
    next_run=now().replace(hour=6, minute=0, second=0, microsecond=0)  # Run daily at 6 AM
)