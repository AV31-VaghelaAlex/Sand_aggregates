from django.urls import path
from . import views

app_name = 'website'

urlpatterns = [
    # Homepage
    path('', views.HomeView.as_view(), name='home'),

    # Product Catalog & Details
    path('products/', views.ProductListView.as_view(), name='products'),
    path('products/<slug:slug>/', views.ProductDetailView.as_view(), name='product_detail'),

    # Ordering System
    path('order/', views.OrderCreateView.as_view(), name='order_create'),
    path('order/<slug:slug>/', views.OrderCreateView.as_view(), name='order_create_product'),
    path('order/success/<str:order_number>/', views.OrderSuccessView.as_view(), name='order_success'),

    # Enquiry System
    path('enquiry/', views.EnquiryCreateView.as_view(), name='enquiry_create'),
    path('enquiry/success/', views.EnquirySuccessView.as_view(), name='enquiry_success_general'),
    path('enquiry/success/<int:enquiry_id>/', views.EnquirySuccessView.as_view(), name='enquiry_success'),

    # Staff Admin Analytics Dashboard
    path('admin-dashboard/', views.AdminDashboardView.as_view(), name='admin_dashboard'),
]
