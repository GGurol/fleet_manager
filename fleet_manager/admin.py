from django.contrib import admin
from .models import Asset, PurchaseDetails, FinancingDetails, LicensingDetails


@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('year', 'make', 'model', 'vehicle_type', 'status', 'vin')
    list_filter = ('status', 'vehicle_type', 'year')
    search_fields = ('vin', 'make', 'model')


@admin.register(PurchaseDetails)
class PurchaseDetailsAdmin(admin.ModelAdmin):
    list_display = ('asset', 'dealership', 'purchase_date',
                    'invoice_no', 'cost_price')
    list_filter = ('dealership', 'purchase_date')
    search_fields = ('invoice_no', 'dealership')


@admin.register(FinancingDetails)
class FinancingDetailsAdmin(admin.ModelAdmin):
    list_display = ('asset', 'funding_institution', 'loan_ref_number',
                    'loan_end_date', 'loan_terms', 'installments')
    list_filter = ('funding_institution', 'loan_end_date')
    search_fields = ('loan_ref_number', 'funding_institution')


@admin.register(LicensingDetails)
class LicensingDetailsAdmin(admin.ModelAdmin):
    list_display = ('asset', 'reg_no', 'fleet_no',
                    'disc_fee', 'disc_expiry_date')
    list_filter = ('disc_expiry_date',)
    search_fields = ('reg_no', 'fleet_no')
