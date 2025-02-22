from django import forms
from .models import User, Asset, PurchaseDetails


class EditProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ["username", "email", "profile_picture"]
        widgets = {
            "username": forms.TextInput(attrs={"class": "form-control", "readonly": "readonly"}),
            "email": forms.EmailInput(attrs={"class": "form-control"}),
            "profile_picture": forms.FileInput(attrs={"class": "form-control"}),
        }


class AssetForm(forms.ModelForm):
    purchase_date = forms.DateField(
        required=True, widget=forms.DateInput(attrs={'type': 'date'}))
    dealership = forms.CharField(required=True, max_length=100)
    invoice_no = forms.CharField(required=True, max_length=100)
    cost_price = forms.DecimalField(
        required=True, max_digits=15, decimal_places=3)
    disc_fee = forms.DecimalField(
        required=False, max_digits=15, decimal_places=3)
    disc_expiry_date = forms.DateField(
        required=False, widget=forms.DateInput(attrs={'type': 'date'}))

    class Meta:
        model = Asset
        fields = ['year', 'make', 'model', 'vehicle_type',
                  'sub_category', 'classification', 'status', 'vin']

    def save(self, commit=True):
        asset = super().save(commit=False)
        if commit:
            asset.save()
            PurchaseDetails.objects.create(
                asset=asset,
                purchase_date=self.cleaned_data['purchase_date'],
                dealership=self.cleaned_data['dealership'],
                invoice_no=self.cleaned_data['invoice_no'],
                cost_price=self.cleaned_data['cost_price']
            )
        return asset
