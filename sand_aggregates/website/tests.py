from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from decimal import Decimal
import copy
from django.template.context import BaseContext

# Python 3.14 compatibility patch for Django 4.2 test client template copying
def _patched_context_copy(self):
    duplicate = object.__new__(self.__class__)
    duplicate.dicts = self.dicts[:]
    return duplicate

BaseContext.__copy__ = _patched_context_copy

from .models import Category, Product, Order, Enquiry, SiteSetting
from .forms import OrderForm, EnquiryForm

User = get_user_model()


class SandAggregatesModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Sand & Fine Aggregates",
            description="Fine sand materials"
        )
        self.product = Product.objects.create(
            name="20mm Aggregate",
            category=self.category,
            short_description="Crushed stone aggregate",
            description="High quality 20mm aggregate for structural casting.",
            price=Decimal('1500.00'),
            unit="Ton",
            available=True,
            featured=True
        )

    def test_category_slug_generation(self):
        self.assertEqual(self.category.slug, "sand-fine-aggregates")

    def test_product_slug_and_formatting(self):
        self.assertEqual(self.product.slug, "20mm-aggregate")
        self.assertEqual(self.product.formatted_price(), "₹1,500.00")

    def test_order_creation_and_calculation(self):
        order = Order.objects.create(
            customer_name="John Doe",
            email="john@example.com",
            phone="+91 98765 43210",
            address="Plot 5, Construction Site Road",
            product=self.product,
            quantity=Decimal('10.00')
        )
        # Price must snapshot product price (1500.00)
        self.assertEqual(order.price, Decimal('1500.00'))
        # Total amount must be 1500 * 10 = 15000.00
        self.assertEqual(order.total_amount, Decimal('15000.00'))
        # Order number must be generated
        self.assertTrue(order.order_number.startswith("ORD-"))
        self.assertEqual(order.status, "Pending")

    def test_enquiry_creation(self):
        enquiry = Enquiry.objects.create(
            name="Jane Smith",
            email="jane@example.com",
            phone="+91 91234 56789",
            product=self.product,
            message="Looking for 50 tons quote"
        )
        self.assertEqual(enquiry.status, "New")
        self.assertIn("Jane Smith", str(enquiry))

    def test_site_setting_singleton(self):
        s1 = SiteSetting.objects.create(business_name="Company One")
        s2 = SiteSetting.objects.create(business_name="Company Two")
        # Due to singleton enforcement, pk is always 1 and count remains 1
        self.assertEqual(SiteSetting.objects.count(), 1)
        self.assertEqual(s2.pk, 1)


class SandAggregatesViewTests(TestCase):
    def setUp(self):
        self.client = Client()
        self.category = Category.objects.create(name="Stone Aggregates")
        self.product = Product.objects.create(
            name="10mm Aggregate",
            category=self.category,
            short_description="10mm crushed stone",
            description="Precast construction aggregate.",
            price=Decimal('1350.00'),
            unit="Ton",
            available=True,
            featured=True
        )
        self.staff_user = User.objects.create_user(
            username="staff_member",
            password="staffpassword",
            is_staff=True
        )

    def test_homepage_view(self):
        response = self.client.get(reverse('website:home'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "10mm Aggregate")
        self.assertContains(response, "₹1,350.00")

    def test_products_list_view(self):
        response = self.client.get(reverse('website:products'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "10mm Aggregate")

    def test_products_list_filter(self):
        response = self.client.get(reverse('website:products') + f'?category={self.category.slug}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "10mm Aggregate")

    def test_product_detail_view(self):
        response = self.client.get(reverse('website:product_detail', kwargs={'slug': self.product.slug}))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "10mm Aggregate")
        self.assertContains(response, "Enquire on WhatsApp")

    def test_order_submission_flow(self):
        order_data = {
            'customer_name': 'Ramesh Kumar',
            'phone': '+91 98765 43210',
            'email': 'ramesh@example.com',
            'address': 'Survey 102, Express Highway Project',
            'product': self.product.id,
            'quantity': '15.0',
            'notes': 'Call driver before arrival',
        }
        response = self.client.post(reverse('website:order_create'), data=order_data)
        self.assertEqual(response.status_code, 302)
        
        # Verify order exists
        order = Order.objects.get(customer_name='Ramesh Kumar')
        self.assertEqual(order.quantity, Decimal('15.0'))
        self.assertEqual(order.total_amount, Decimal('20250.00')) # 1350 * 15

        # Test Order Success page
        success_response = self.client.get(reverse('website:order_success', kwargs={'order_number': order.order_number}))
        self.assertEqual(success_response.status_code, 200)
        self.assertContains(success_response, order.order_number)

    def test_enquiry_submission_flow(self):
        enquiry_data = {
            'name': 'Pooja Verma',
            'phone': '+91 98250 99999',
            'email': 'pooja@company.com',
            'product': self.product.id,
            'message': 'Need test certificate and quote for 100 Tons',
        }
        response = self.client.post(reverse('website:enquiry_create'), data=enquiry_data)
        self.assertEqual(response.status_code, 302)
        self.assertTrue(Enquiry.objects.filter(name='Pooja Verma').exists())

    def test_admin_dashboard_security(self):
        # Unauthenticated user should be redirected to admin login
        response = self.client.get(reverse('website:admin_dashboard'))
        self.assertEqual(response.status_code, 302)

        # Staff user should be able to view dashboard
        self.client.login(username="staff_member", password="staffpassword")
        response = self.client.get(reverse('website:admin_dashboard'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Business & Logistics Dashboard")


class SandAggregatesFormTests(TestCase):
    def test_order_form_validation(self):
        form = OrderForm(data={
            'customer_name': 'Test User',
            'phone': '123', # Invalid short phone
            'email': 'invalid-email',
            'address': 'Test Address',
            'quantity': '-5', # Invalid negative quantity
        })
        self.assertFalse(form.is_valid())
        self.assertIn('phone', form.errors)
        self.assertIn('email', form.errors)
        self.assertIn('quantity', form.errors)
