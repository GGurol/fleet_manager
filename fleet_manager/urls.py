from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('assets/', views.asset_list, name='asset_list'),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path("edit_profile/", views.edit_profile, name="edit_profile"),
    path('trucks/', views.truck_list, name='truck_list'),
    path('trailers/', views.trailer_list, name='trailer_list'),
    path('light/', views.light_list, name='light_list'),
    path('inactive/', views.inactive_list, name='inactive_list'),
    path('finance/', views.finance_summary, name='finance_summary'),
    path('license/', views.licensing, name='licensing'),
    path('asset/<int:asset_id>/', views.asset_view, name='asset-detail'),
    path('search/', views.search_view, name='search'),
    path('add-asset/', views.add_asset, name='add_asset'),
    path('asset/<int:asset_id>/edit/', views.edit_asset_view, name='edit_asset'),
    path('assets/export/', views.export_assets, name='export_assets'),
]
