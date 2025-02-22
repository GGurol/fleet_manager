from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.db import IntegrityError
from django.core.paginator import Paginator
from datetime import date, timedelta

from .models import User, Asset, PurchaseDetails, FinancingDetails, LicensingDetails
from django.db.models import Sum, Count

from .forms import EditProfileForm, AssetForm


def home(request):
    # Count and total cost per vehicle type
    vehicle_summary = Asset.objects.values('vehicle_type').annotate(
        total_cost=Sum('purchasedetails__cost_price'),
        count=Count('id')
    ).order_by('vehicle_type')

    # Finance house and count for financed vehicles
    financed_data = FinancingDetails.objects.values('funding_institution').annotate(
        count=Count('id')
    ).order_by('funding_institution')

    context = {
        'vehicle_summary': vehicle_summary,
        'financed_data': financed_data,
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

    paginator = Paginator(assets, 10)
    page_number = request.GET.get("page")
    assets = paginator.get_page(page_number)
    return render(request, 'fleet_manager/asset_list.html', {'assets': assets})


def truck_list(request):
    filtered_assets = Asset.objects.filter(
        vehicle_type='Truck', status='Active')
    return render(request, 'fleet_manager/asset_list.html', {'assets': filtered_assets})


def trailer_list(request):
    filtered_assets = Asset.objects.filter(
        vehicle_type='Trailer', status='Active')
    return render(request, 'fleet_manager/asset_list.html', {'assets': filtered_assets})


def light_list(request):
    filtered_assets = Asset.objects.filter(
        vehicle_type='Light Vehicle', status='Active')
    return render(request, 'fleet_manager/asset_list.html', {'assets': filtered_assets})


def inactive_list(request):
    filtered_assets = Asset.objects.filter(status='Inactive')
    return render(request, 'fleet_manager/asset_list.html', {'assets': filtered_assets})


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

    paginator = Paginator(discs, 12)
    page_number = request.GET.get("page")
    discs = paginator.get_page(page_number)

    return render(request, 'fleet_manager/licensing.html', {'discs': discs})


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
