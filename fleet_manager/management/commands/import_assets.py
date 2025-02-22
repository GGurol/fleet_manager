import csv
import os
from datetime import datetime
from django.core.management.base import BaseCommand
from fleet_manager.models import Asset, PurchaseDetails, FinancingDetails, LicensingDetails
from django.core.exceptions import ValidationError


class Command(BaseCommand):
    help = 'Import assets from a CSV file'

    def convert_date_format(self, date_str, input_format='%Y/%m/%d', output_format='%Y-%m-%d'):
        """Converts date from CSV to match Django's format, returns None if empty"""
        if not date_str or date_str.strip() == '':
            return None
        try:
            date_obj = datetime.strptime(date_str, input_format)
            return date_obj.strftime(output_format)
        except ValueError:
            print(
                f'Invalid date format: {date_str}. Expected format: yyyy/mm/dd')
            return None

    def handle_decimal_field(self, value):
        """Handles decimal values from CSV, returns None if empty"""
        if not value or value.strip() == '':
            return None  # Use None instead of 0.00 if empty
        try:
            return round(float(value), 3)
        except ValueError:
            print(f"Invalid decimal value: {value}. Defaulting to None.")
            return None

    def handle_integer_field(self, value):
        """Handles integer values from CSV, returns None if empty"""
        if not value or value.strip() == '':
            return None  # Use None instead of 0 if empty
        try:
            return int(value)
        except ValueError:
            print(f"Invalid integer value: {value}. Defaulting to None.")
            return None

    def handle(self, *args, **kwargs):
        base_dir = os.path.dirname(os.path.abspath(__file__))
        csv_file_path = os.path.join(base_dir, 'initial_fleet.csv')

        with open(csv_file_path, newline='', encoding='utf-8-sig') as csvfile:
            reader = csv.DictReader(csvfile)

            print("Column Names:", reader.fieldnames)

            for row in reader:
                try:
                    # Convert dates
                    purchase_date = self.convert_date_format(
                        row.get('purchase_date'))
                    disc_expiry_date = self.convert_date_format(
                        row.get('disc_expiry_date'))
                    loan_end_date = self.convert_date_format(
                        row.get('loan_end_date'))

                    # Process numeric fields
                    cost_price = self.handle_decimal_field(
                        row.get('cost_price'))
                    disc_fee = self.handle_decimal_field(row.get('disc_fee'))
                    installments = self.handle_decimal_field(
                        row.get('installments'))
                    loan_terms = self.handle_integer_field(
                        row.get('loan_terms'))

                    # Create Asset
                    asset = Asset.objects.create(
                        year=self.handle_integer_field(row.get('year')),
                        make=row.get('make'),
                        model=row.get('model'),
                        vehicle_type=row.get('vehicle_type'),
                        sub_category=row.get('sub_category'),
                        classification=row.get('classification'),
                        status=row.get('status'),
                        vin=row.get('vin'),
                    )

                    # Create PurchaseDetails
                    PurchaseDetails.objects.create(
                        purchase_date=purchase_date,
                        dealership=row.get('dealership'),
                        invoice_no=row.get('invoice_no'),
                        cost_price=cost_price,
                        asset=asset
                    )

                    # Only create FinancingDetails if loan info is present
                    if row.get('funding_institution') or loan_terms or installments:
                        FinancingDetails.objects.create(
                            funding_institution=row.get(
                                'funding_institution') or None,
                            loan_ref_number=row.get('loan_ref_number') or None,
                            loan_end_date=loan_end_date,
                            loan_terms=loan_terms,
                            installments=installments,
                            asset=asset
                        )

                    # Only create LicensingDetails if reg_no or fleet_no is present
                    if row.get('reg_no') or row.get('fleet_no'):
                        LicensingDetails.objects.create(
                            reg_no=row.get('reg_no') or None,
                            fleet_no=row.get('fleet_no') or None,
                            disc_fee=disc_fee,
                            disc_expiry_date=disc_expiry_date,
                            asset=asset
                        )

                except ValidationError as e:
                    print(f"Validation Error: {e} in row: {row}")
