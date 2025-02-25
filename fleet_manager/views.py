from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.core.paginator import Paginator
from datetime import date, timedelta, datetime
from django.db.models.functions import ExtractMonth
import csv

from .models import User, Asset, PurchaseDetails, FinancingDetails, LicensingDetails
from django.db.models import Sum, Count

from .forms import EditProfileForm, AssetForm


def home(request):
    # Count and total cost per vehicle type
    vehicle_summary = Asset.objects.filter(status='Active').values('vehicle_type').annotate(
        total_cost=Sum('purchasedetails__cost_price'),
        count=Count('id')
    ).order_by('vehicle_type')

    # Calculate overall totals
    total_count = sum(item['count'] for item in vehicle_summary)
    total_cost = sum(item['total_cost'] for item in vehicle_summary if item['total_cost'] is not None)

    context = {
        'vehicle_summary': vehicle_summary,
        'total_count': total_count,
        'total_cost': total_cost,
    }

    return render(request, 'fleet_manager/home.html', context)


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("home"))
        else:
            return render(request, "fleet_manager/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "fleet_manager/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("home"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        profile_picture = request.FILES.get(
            "profile_picture")  # Get uploaded file

        # Ensure password matches confirmation
        if password != confirmation:
            return render(request, "fleet_manager/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create a new user
        try:
            user = User.objects.create_user(username, email, password)
            if profile_picture:
                user.profile_picture = profile_picture  # Assign profile picture
            else:
                user.profile_picture = "profile_pics/avator.png"  # Default avatar

            user.save()
        except IntegrityError:
            return render(request, "fleet_manager/register.html", {
                "message": "Username already taken."
            })

        login(request, user)
        return HttpResponseRedirect(reverse("home"))

    return render(request, "fleet_manager/register.html")


@login_required
def edit_profile(request):
    if request.method == "POST":
        form = EditProfileForm(
            request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(
                request, "Your profile has been updated successfully!")
            return redirect("edit_profile")
    else:
        form = EditProfileForm(instance=request.user)

    return render(request, "fleet_manager/edit_profile.html", {"form": form})


def asset_list(request):
    assets = Asset.objects.filter(status='Active')
    title = "All Assets"
    export_url = reverse('export_assets') + "?vehicle_type=all"

    paginator = Paginator(assets, 10)
    page_number = request.GET.get("page")
    assets = paginator.get_page(page_number)

    return render(request, 'fleet_manager/asset_list.html', {'assets': assets, 'title': title, 'export_url': export_url})


def truck_list(request):
    filtered_assets = Asset.objects.filter(vehicle_type='Truck', status='Active')
    title = "Trucks"
    export_url = reverse('export_assets') + "?vehicle_type=truck"

    paginator = Paginator(filtered_assets, 10)
    page_number = request.GET.get("page")
    filtered_assets = paginator.get_page(page_number)

    return render(request, 'fleet_manager/asset_list.html', {'assets': filtered_assets, 'title': title, 'export_url': export_url})


def trailer_list(request):
    filtered_assets = Asset.objects.filter(vehicle_type='Trailer', status='Active')
    title = "Trailers"
    export_url = reverse('export_assets') + "?vehicle_type=trailer"

    paginator = Paginator(filtered_assets, 10)
    page_number = request.GET.get("page")
    filtered_assets = paginator.get_page(page_number)

    return render(request, 'fleet_manager/asset_list.html', {'assets': filtered_assets, 'title': title, 'export_url': export_url})


def light_list(request):
    filtered_assets = Asset.objects.filter(vehicle_type='Light Vehicle', status='Active')
    title = "Light Vehicles"
    export_url = reverse('export_assets') + "?vehicle_type=light"

    paginator = Paginator(filtered_assets, 10)
    page_number = request.GET.get("page")
    filtered_assets = paginator.get_page(page_number)

    return render(request, 'fleet_manager/asset_list.html', {'assets': filtered_assets, 'title': title, 'export_url': export_url})


def inactive_list(request):
    filtered_assets = Asset.objects.filter(status='Inactive')
    title = "Inactive Vehicles"
    export_url = reverse('export_assets') + "?vehicle_type=inactive"

    paginator = Paginator(filtered_assets, 10)
    page_number = request.GET.get("page")
    filtered_assets = paginator.get_page(page_number)

    return render(request, 'fleet_manager/asset_list.html', {'assets': filtered_assets, 'title': title, 'export_url': export_url})


def finance_summary(request):
    financed_data = FinancingDetails.objects.values('funding_institution').annotate(
        count=Count('id'),  # Count of assets financed by this institution
        # Sum of installments for this institution
        total_installments=Sum('installments')
    )

    context = {
        'financed_data': financed_data,
    }

    return render(request, 'fleet_manager/finance.html', context)


def licensing(request):
    today = date.today()
    today_plus_30 = today + timedelta(days=30)

    discs = LicensingDetails.objects.all().order_by('disc_expiry_date')  

    for disc in discs:
        disc.is_expiring_soon = disc.disc_expiry_date and disc.disc_expiry_date <= today_plus_30

    paginator = Paginator(discs, 5)
    page_number = request.GET.get("page")
    discs = paginator.get_page(page_number)

     # Aggregate expiry data by month
    monthly_expiries = (
        LicensingDetails.objects
        .values(month=ExtractMonth('disc_expiry_date'))
        .annotate(
            num_vehicles=Count('id'),
            total_fees=Sum('disc_fee')
        )
        .order_by('month')
    )

    # Convert month number to name (e.g., 1 → January)
    month_map = {i: datetime(2000, i, 1).strftime('%B') for i in range(1, 13)}
    monthly_summary = [
        {
            "month": month_map.get(item["month"], "Unknown"),
            "num_vehicles": item["num_vehicles"],
            "total_fees": item["total_fees"] or 0  # Ensure no None values
        }
        for item in monthly_expiries
    ]

    return render(request, 'fleet_manager/licensing.html', {'discs': discs, 'monthly_summary': monthly_summary})


def asset_view(request, asset_id):
    # Get the asset or return a 404 error if not found
    asset = get_object_or_404(Asset, id=asset_id)

    # Fetch related data
    purchase_details = PurchaseDetails.objects.filter(asset=asset).first()
    financing_details = FinancingDetails.objects.filter(asset=asset)
    licensing_details = LicensingDetails.objects.filter(asset=asset)

    context = {
        "asset": asset,
        "purchase_details": purchase_details,
        "financing_details": financing_details,
        "licensing_details": licensing_details,
    }

    return render(request, "fleet_manager/asset_screen.html", context)


def search_view(request):
    query = request.GET.get('q', '')
    if query:
        # Perform search query including VIN
        results = Asset.objects.filter(
            make__icontains=query
        ) | Asset.objects.filter(
            model__icontains=query
        ) | Asset.objects.filter(
            vin__icontains=query
        )
    else:
        results = Asset.objects.none()

    context = {
        'results': results,
        'query': query
    }

    return render(request, 'fleet_manager/search.html', context)


@login_required
def add_asset(request):
    if request.method == "POST":
        form = AssetForm(request.POST)
        if form.is_valid():
            asset = form.save()
            # ✅ Correct redirect
            return redirect('asset-detail', asset_id=asset.id)
        else:
            print(form.errors)  # 🔍 Debugging: Print errors to console
    else:
        form = AssetForm()

    return render(request, 'fleet_manager/add_asset_modal.html', {'form': form})


def edit_asset_view(request, asset_id):
    asset = get_object_or_404(Asset, id=asset_id)

    if request.method == 'POST':
        # Admins can edit the asset
        if request.user.is_superuser:
            asset.year = request.POST.get('year')
            asset.make = request.POST.get('make')
            asset.model = request.POST.get('model')
            asset.vehicle_type = request.POST.get('vehicle_type')
            asset.sub_category = request.POST.get('sub_category')
            asset.classification = request.POST.get('classification')
            asset.status = request.POST.get('status')
            # VIN is not editable and not included here
            asset.save()
            return redirect('asset-detail', asset_id=asset.id)

    context = {'asset': asset}
    
    return render(request, 'fleet_manager/asset_screen.html', context)


def export_assets(request):
    """Exports filtered assets to a CSV file based on the vehicle type query parameter."""

    vehicle_type = request.GET.get("vehicle_type", "all")  # Default to "all"
    filename = "all_assets.csv"

    if vehicle_type == "all":
        assets = Asset.objects.filter(status="Active")
    elif vehicle_type == "truck":
        assets = Asset.objects.filter(vehicle_type="Truck", status="Active")
        filename = "trucks.csv"
    elif vehicle_type == "trailer":
        assets = Asset.objects.filter(vehicle_type="Trailer", status="Active")
        filename = "trailers.csv"
    elif vehicle_type == "light":
        assets = Asset.objects.filter(vehicle_type="Light Vehicle", status="Active")
        filename = "light_vehicles.csv"
    elif vehicle_type == "inactive":
        assets = Asset.objects.filter(status="Inactive")
        filename = "inactive_assets.csv"
    else:
        assets = Asset.objects.filter(status="Active")

    # Create CSV response
    response = HttpResponse(content_type="text/csv")
    response["Content-Disposition"] = f'attachment; filename="{filename}"'

    writer = csv.writer(response)
    writer.writerow(["Make", "Model", "Year", "Type", "Status"])

    for asset in assets:
        writer.writerow([asset.make, asset.model, asset.year, asset.vehicle_type, asset.status])

    return response