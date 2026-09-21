from django.contrib import admin
from django.utils.html import mark_safe
from .models import Category, Product, Order, Enquiry, SiteSetting


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    search_fields = ('name', 'description')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('is_active',)


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ('image_preview', 'name', 'category', 'price', 'unit', 'available', 'featured', 'updated_at')
    list_display_links = ('name',)
    list_editable = ('price', 'available', 'featured')
    search_fields = ('name', 'short_description', 'description')
    list_filter = ('category', 'available', 'featured', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('image_preview_large', 'created_at', 'updated_at')
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'available', 'featured')
        }),
        ('Pricing & Measurement', {
            'fields': ('price', 'unit')
        }),
        ('Descriptions', {
            'fields': ('short_description', 'description')
        }),
        ('Product Media', {
            'fields': ('image', 'image_preview_large')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="width: 48px; height: 38px; object-fit: cover; border-radius: 4px;" />')
        return mark_safe('<span style="color: #888;">No image</span>')
    image_preview.short_description = 'Photo'

    def image_preview_large(self, obj):
        if obj.image:
            return mark_safe(f'<img src="{obj.image.url}" style="max-width: 320px; max-height: 240px; object-fit: cover; border-radius: 6px;" />')
        return "No image uploaded"
    image_preview_large.short_description = 'Current Image'


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'order_number',
        'customer_name',
        'phone',
        'product',
        'quantity',
        'total_amount',
        'status',
        'created_at',
    )
    list_filter = ('status', 'created_at', 'product')
    search_fields = ('order_number', 'customer_name', 'phone', 'email', 'address')
    list_editable = ('status',)
    readonly_fields = ('order_number', 'price', 'total_amount', 'created_at', 'updated_at')
    date_hierarchy = 'created_at'
    actions = ['mark_confirmed', 'mark_processing', 'mark_delivered', 'mark_cancelled']

    fieldsets = (
        ('Order Identification', {
            'fields': ('order_number', 'status', 'created_at', 'updated_at')
        }),
        ('Customer Details', {
            'fields': ('customer_name', 'phone', 'email', 'address')
        }),
        ('Material & Financials', {
            'fields': ('product', 'quantity', 'price', 'total_amount')
        }),
        ('Additional Notes', {
            'fields': ('notes',)
        }),
    )

    @admin.action(description="Mark selected orders as Confirmed")
    def mark_confirmed(self, request, queryset):
        queryset.update(status='Confirmed')

    @admin.action(description="Mark selected orders as Processing/Dispatched")
    def mark_processing(self, request, queryset):
        queryset.update(status='Processing')

    @admin.action(description="Mark selected orders as Delivered")
    def mark_delivered(self, request, queryset):
        queryset.update(status='Delivered')

    @admin.action(description="Mark selected orders as Cancelled")
    def mark_cancelled(self, request, queryset):
        queryset.update(status='Cancelled')


@admin.register(Enquiry)
class EnquiryAdmin(admin.ModelAdmin):
    list_display = ('name', 'phone', 'email', 'product_display', 'quantity', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('name', 'phone', 'email', 'company', 'message', 'location')
    list_editable = ('status',)
    readonly_fields = ('created_at',)
    date_hierarchy = 'created_at'
    actions = ['mark_contacted', 'mark_closed']

    def product_display(self, obj):
        if obj.product:
            return obj.product.name
        return obj.product_name or "-"
    product_display.short_description = 'Product / Material'

    @admin.action(description="Mark selected enquiries as Contacted")
    def mark_contacted(self, request, queryset):
        queryset.update(status='Contacted')

    @admin.action(description="Mark selected enquiries as Closed")
    def mark_closed(self, request, queryset):
        queryset.update(status='Closed')


@admin.register(SiteSetting)
class SiteSettingAdmin(admin.ModelAdmin):
    list_display = ('business_name', 'phone_display', 'whatsapp_number', 'email')
    fieldsets = (
        ('Business Branding', {
            'fields': ('business_name', 'tagline')
        }),
        ('Direct Contact', {
            'fields': ('phone_display', 'phone_raw', 'email', 'address', 'business_hours')
        }),
        ('WhatsApp Integration', {
            'fields': ('whatsapp_number', 'whatsapp_default_message'),
            'description': 'Configure the WhatsApp contact digits and default inquiry message.'
        }),
        ('Google Maps & Social Media', {
            'fields': ('google_maps_url', 'instagram_url', 'linkedin_url')
        }),
    )

    def has_add_permission(self, request):
        # Prevent creating multiple setting instances
        return not SiteSetting.objects.exists()

    def has_delete_permission(self, request, obj=None):
        return False
