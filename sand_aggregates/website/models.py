from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from decimal import Decimal
import uuid
from datetime import datetime


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=120, unique=True, blank=True)
    description = models.TextField(blank=True, help_text="Brief description of this material category")
    order = models.PositiveIntegerField(default=0, help_text="Display order in menus and filters")
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ['order', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Product(models.Model):
    UNIT_CHOICES = [
        ('Ton', 'Ton'),
        ('Truck', 'Truck (Full Load)'),
        ('Cubic Meter', 'Cubic Meter (m³)'),
        ('Brass', 'Brass'),
        ('Bag', 'Bag (50 kg)'),
    ]

    name = models.CharField(max_length=150, unique=True)
    slug = models.SlugField(max_length=170, unique=True, blank=True)
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        related_name='products',
        null=True,
        blank=True
    )
    image = models.ImageField(
        upload_to='products/',
        blank=True,
        null=True,
        help_text="Upload high quality product photo"
    )
    short_description = models.CharField(
        max_length=255,
        help_text="Short one-line summary displayed on product cards"
    )
    description = models.TextField(
        help_text="Detailed specification, uses, grading, and material properties"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        help_text="Price per unit in INR (₹)"
    )
    unit = models.CharField(
        max_length=50,
        choices=UNIT_CHOICES,
        default='Ton'
    )
    available = models.BooleanField(
        default=True,
        help_text="Is this material currently in stock and available for delivery?"
    )
    featured = models.BooleanField(
        default=False,
        help_text="Display prominently on the homepage products showcase"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-featured', 'name']

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('website:product_detail', kwargs={'slug': self.slug})

    def formatted_price(self):
        return f"₹{self.price:,.2f}"

    def __str__(self):
        return f"{self.name} - ₹{self.price}/{self.unit}"


class Order(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending (New)'),
        ('Confirmed', 'Confirmed'),
        ('Processing', 'Processing / Dispatched'),
        ('Delivered', 'Delivered'),
        ('Cancelled', 'Cancelled'),
    ]

    order_number = models.CharField(max_length=30, unique=True, editable=False)
    customer_name = models.CharField(max_length=120)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    address = models.TextField(help_text="Delivery site address, landmark, or location")
    product = models.ForeignKey(
        Product,
        on_delete=models.PROTECT,
        related_name='orders'
    )
    quantity = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=1.00,
        help_text="Quantity in product units"
    )
    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        editable=False,
        help_text="Unit price snapshot at order submission"
    )
    total_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        editable=False,
        help_text="Calculated: price * quantity"
    )
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='Pending'
    )
    notes = models.TextField(
        blank=True,
        help_text="Special delivery instructions, timing, or dump truck access notes"
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        # Snapshot product unit price and calculate total
        if self.product:
            if not self.price:
                self.price = self.product.price
            self.total_amount = Decimal(str(self.price)) * Decimal(str(self.quantity))

        # Generate unique order number if empty
        if not self.order_number:
            year = datetime.now().year
            # Get latest order id
            latest = Order.objects.order_by('-id').first()
            next_num = (latest.id + 1) if latest else 1
            self.order_number = f"ORD-{year}-{next_num:04d}"

        super().save(*args, **kwargs)

    def formatted_total(self):
        return f"₹{self.total_amount:,.2f}"

    def __str__(self):
        return f"{self.order_number} - {self.customer_name} ({self.status})"


class Enquiry(models.Model):
    STATUS_CHOICES = [
        ('New', 'New Enquiry'),
        ('Contacted', 'Contacted / Quotation Sent'),
        ('Closed', 'Closed / Converted'),
    ]

    name = models.CharField(max_length=120)
    email = models.EmailField(blank=True)
    phone = models.CharField(max_length=20)
    company = models.CharField(max_length=150, blank=True, help_text="Company or builder firm")
    product = models.ForeignKey(
        Product,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='enquiries'
    )
    product_name = models.CharField(max_length=150, blank=True, help_text="Product or material name")
    quantity = models.CharField(max_length=50, blank=True, help_text="Requested quantity")
    unit = models.CharField(max_length=50, blank=True, help_text="e.g. Ton, Truck, Brass")
    location = models.CharField(max_length=255, blank=True, help_text="Delivery destination")
    message = models.TextField(help_text="Specific requirements, quality grading, or site timeline")
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='New')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = "Enquiries"
        ordering = ['-created_at']

    def __str__(self):
        prod = self.product.name if self.product else (self.product_name or "General")
        return f"Enquiry from {self.name} for {prod} ({self.status})"


class SiteSetting(models.Model):
    """
    Singleton model for configurable contact info, WhatsApp, social channels and maps.
    Allows admin to customize without code edits.
    """
    business_name = models.CharField(max_length=150, default="LJ ENTERPRISE")
    tagline = models.CharField(
        max_length=255,
        default="At the heart of every strong structure lies a solid foundation — and that starts with quality materials."
    )
    phone_display = models.CharField(max_length=30, default="+91 81413 52886")
    phone_raw = models.CharField(max_length=30, default="+918141352886", help_text="Digits with country code, no spaces for tel: link")
    whatsapp_number = models.CharField(max_length=30, default="918141352886", help_text="Digits only with country code (e.g. 918141352886) for wa.me links")
    email = models.EmailField(default="infoljenterprise07@gmail.com")
    address = models.CharField(max_length=255, default="Ahmedabad, Gujarat, India")
    business_hours = models.CharField(max_length=100, default="Open 24 hours")
    google_maps_url = models.URLField(max_length=500, default="https://www.google.com/maps?q=Ahmedabad,Gujarat,India&output=embed")
    whatsapp_default_message = models.TextField(
        default="Hello LJ Enterprise, I am interested in your sand, GSB, and aggregates materials. Please share pricing and availability."
    )
    # Social links
    instagram_url = models.URLField(default="https://www.instagram.com/infoljenterprise?stkn=MWd3cGN3dDV6Ym44aA==", blank=True)
    linkedin_url = models.URLField(default="https://www.linkedin.com/company/rashienterprise", blank=True)

    class Meta:
        verbose_name = "Business Configuration & Contact Settings"
        verbose_name_plural = "Business Configuration & Contact Settings"

    def save(self, *args, **kwargs):
        # Enforce singleton pattern
        self.pk = 1
        if SiteSetting.objects.filter(pk=1).exists():
            kwargs.pop('force_insert', None)
        super().save(*args, **kwargs)

    @classmethod
    def get_settings(cls):
        obj, _ = cls.objects.get_or_create(pk=1)
        return obj

    def __str__(self):
        return f"{self.business_name} Site Configuration"
