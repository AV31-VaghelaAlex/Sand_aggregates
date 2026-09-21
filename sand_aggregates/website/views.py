from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import View, ListView, DetailView
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from django.utils.decorators import method_decorator
from django.db.models import Count, Sum, Q
import urllib.parse
from decimal import Decimal

from .models import Product, Category, Order, Enquiry, SiteSetting
from .forms import OrderForm, EnquiryForm


class HomeView(View):
    template_name = 'home.html'

    def get(self, request):
        featured_products = Product.objects.filter(available=True, featured=True)[:8]
        # If no featured products marked, grab all available products
        if not featured_products.exists():
            featured_products = Product.objects.filter(available=True)[:8]

        categories = Category.objects.filter(is_active=True).annotate(
            prod_count=Count('products', filter=Q(products__available=True))
        )
        enquiry_form = EnquiryForm()

        context = {
            'featured_products': featured_products,
            'categories': categories,
            'enquiry_form': enquiry_form,
        }
        return render(request, self.template_name, context)

    def post(self, request):
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            messages.success(request, "Thank you! Your enquiry has been submitted successfully. Our team will contact you shortly.")
            return redirect('website:enquiry_success', enquiry_id=enquiry.id)
        
        # If form is invalid, re-render home with errors
        featured_products = Product.objects.filter(available=True, featured=True)[:8]
        if not featured_products.exists():
            featured_products = Product.objects.filter(available=True)[:8]
        categories = Category.objects.filter(is_active=True)

        context = {
            'featured_products': featured_products,
            'categories': categories,
            'enquiry_form': form,
        }
        return render(request, self.template_name, context)


class ProductListView(ListView):
    model = Product
    template_name = 'products.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.all()
        category_slug = self.request.GET.get('category')
        query = self.request.GET.get('q')

        if category_slug:
            queryset = queryset.filter(category__slug=category_slug)
        if query:
            queryset = queryset.filter(
                Q(name__icontains=query) |
                Q(short_description__icontains=query) |
                Q(description__icontains=query)
            )
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.filter(is_active=True)
        context['current_category'] = self.request.GET.get('category', '')
        context['search_query'] = self.request.GET.get('q', '')
        return context


class ProductDetailView(DetailView):
    model = Product
    template_name = 'product_detail.html'
    context_object_name = 'product'
    slug_url_kwarg = 'slug'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product = self.object

        # Related products
        related = Product.objects.filter(category=product.category).exclude(id=product.id)[:4]
        if not related.exists():
            related = Product.objects.exclude(id=product.id)[:4]

        # WhatsApp pre-filled message for this specific product
        site_config = SiteSetting.get_settings()
        product_msg = (
            f"Hello, I am interested in ordering:\n\n"
            f"Product: {product.name}\n"
            f"Price: {product.formatted_price()} / {product.unit}\n\n"
            f"Please share availability and delivery terms."
        )
        whatsapp_product_url = f"https://wa.me/{site_config.whatsapp_number}?text={urllib.parse.quote(product_msg)}"

        context['related_products'] = related
        context['whatsapp_product_url'] = whatsapp_product_url
        context['enquiry_form'] = EnquiryForm(initial={'product': product, 'product_name': product.name})
        return context


class OrderCreateView(View):
    template_name = 'order.html'

    def get(self, request, slug=None):
        initial_data = {}
        selected_product = None
        if slug:
            selected_product = get_object_or_404(Product, slug=slug, available=True)
            initial_data['product'] = selected_product

        form = OrderForm(initial=initial_data)
        products = Product.objects.filter(available=True)
        context = {
            'form': form,
            'selected_product': selected_product,
            'products': products,
        }
        return render(request, self.template_name, context)

    def post(self, request, slug=None):
        form = OrderForm(request.POST)
        if form.is_valid():
            order = form.save()
            messages.success(request, f"Order #{order.order_number} submitted successfully!")
            return redirect('website:order_success', order_number=order.order_number)
        
        products = Product.objects.filter(available=True)
        selected_product = None
        if slug:
            selected_product = Product.objects.filter(slug=slug).first()

        context = {
            'form': form,
            'selected_product': selected_product,
            'products': products,
        }
        return render(request, self.template_name, context)


class OrderSuccessView(DetailView):
    model = Order
    template_name = 'order_success.html'
    context_object_name = 'order'
    slug_field = 'order_number'
    slug_url_kwarg = 'order_number'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        order = self.object
        site_config = SiteSetting.get_settings()
        
        # WhatsApp link to ping admin regarding this specific order
        order_msg = (
            f"Hello, I have placed an order on your website:\n\n"
            f"Order Number: {order.order_number}\n"
            f"Customer: {order.customer_name}\n"
            f"Product: {order.product.name}\n"
            f"Quantity: {order.quantity} {order.product.unit}\n"
            f"Total Amount: {order.formatted_total()}\n\n"
            f"Please confirm delivery schedule."
        )
        context['whatsapp_order_url'] = f"https://wa.me/{site_config.whatsapp_number}?text={urllib.parse.quote(order_msg)}"
        return context


class EnquiryCreateView(View):
    template_name = 'enquiry.html'

    def get(self, request):
        product_id = request.GET.get('product')
        initial = {}
        if product_id:
            try:
                prod = Product.objects.get(id=product_id)
                initial['product'] = prod
                initial['product_name'] = prod.name
            except Product.DoesNotExist:
                pass
        form = EnquiryForm(initial=initial)
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = EnquiryForm(request.POST)
        if form.is_valid():
            enquiry = form.save()
            messages.success(request, "Your enquiry has been received successfully!")
            return redirect('website:enquiry_success', enquiry_id=enquiry.id)
        return render(request, self.template_name, {'form': form})


class EnquirySuccessView(View):
    template_name = 'enquiry_success.html'

    def get(self, request, enquiry_id=None):
        enquiry = None
        if enquiry_id:
            enquiry = get_object_or_404(Enquiry, id=enquiry_id)
        return render(request, self.template_name, {'enquiry': enquiry})


@method_decorator(user_passes_test(lambda u: u.is_staff, login_url='/admin/login/'), name='dispatch')
class AdminDashboardView(View):
    template_name = 'admin_dashboard.html'

    def get(self, request):
        total_products = Product.objects.count()
        available_products = Product.objects.filter(available=True).count()
        total_orders = Order.objects.count()
        pending_orders = Order.objects.filter(status='Pending').count()
        confirmed_orders = Order.objects.filter(status='Confirmed').count()
        delivered_orders = Order.objects.filter(status='Delivered').count()
        cancelled_orders = Order.objects.filter(status='Cancelled').count()
        total_revenue = Order.objects.exclude(status='Cancelled').aggregate(Sum('total_amount'))['total_amount__sum'] or Decimal('0.00')

        total_enquiries = Enquiry.objects.count()
        new_enquiries = Enquiry.objects.filter(status='New').count()

        recent_orders = Order.objects.select_related('product').order_by('-created_at')[:8]
        recent_enquiries = Enquiry.objects.select_related('product').order_by('-created_at')[:8]

        # Chart Data
        order_status_labels = ['Pending', 'Confirmed', 'Processing', 'Delivered', 'Cancelled']
        order_status_counts = [
            Order.objects.filter(status='Pending').count(),
            Order.objects.filter(status='Confirmed').count(),
            Order.objects.filter(status='Processing').count(),
            Order.objects.filter(status='Delivered').count(),
            Order.objects.filter(status='Cancelled').count(),
        ]

        enquiry_status_labels = ['New', 'Contacted', 'Closed']
        enquiry_status_counts = [
            Enquiry.objects.filter(status='New').count(),
            Enquiry.objects.filter(status='Contacted').count(),
            Enquiry.objects.filter(status='Closed').count(),
        ]

        context = {
            'total_products': total_products,
            'available_products': available_products,
            'total_orders': total_orders,
            'pending_orders': pending_orders,
            'confirmed_orders': confirmed_orders,
            'delivered_orders': delivered_orders,
            'total_revenue': total_revenue,
            'total_enquiries': total_enquiries,
            'new_enquiries': new_enquiries,
            'recent_orders': recent_orders,
            'recent_enquiries': recent_enquiries,
            'order_status_labels': order_status_labels,
            'order_status_counts': order_status_counts,
            'enquiry_status_labels': enquiry_status_labels,
            'enquiry_status_counts': enquiry_status_counts,
        }
        return render(request, self.template_name, context)
