from django import forms
from django.core.exceptions import ValidationError
import re
from .models import Order, Enquiry, Product


class OrderForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ['customer_name', 'phone', 'email', 'address', 'product', 'quantity', 'notes']
        widgets = {
            'customer_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter your full name',
                'required': True,
                'autocomplete': 'name',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': '+91 98765 43210',
                'required': True,
                'autocomplete': 'tel',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'name@example.com',
                'required': True,
                'autocomplete': 'email',
            }),
            'address': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 3,
                'placeholder': 'Delivery site address, plot/road number, nearest landmark...',
                'required': True,
            }),
            'product': forms.Select(attrs={
                'class': 'form-select',
                'required': True,
                'id': 'order-product-select',
            }),
            'quantity': forms.NumberInput(attrs={
                'class': 'form-control',
                'min': '0.5',
                'step': '0.5',
                'value': '1.0',
                'required': True,
                'id': 'order-quantity-input',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 2,
                'placeholder': 'Unloading instructions, dump truck access timing, specific grading preferences...',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only list available products in the select dropdown
        self.fields['product'].queryset = Product.objects.filter(available=True)
        self.fields['product'].empty_label = "Select a construction material"

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        cleaned_phone = re.sub(r'[\s\-\(\)\.]', '', phone)
        if len(cleaned_phone) < 10 or not re.match(r'^\+?[0-9]{10,15}$', cleaned_phone):
            raise ValidationError("Please provide a valid 10-digit mobile number with country code.")
        return phone

    def clean_quantity(self):
        qty = self.cleaned_data.get('quantity')
        if qty is None or qty <= 0:
            raise ValidationError("Quantity must be greater than zero.")
        return qty


class EnquiryForm(forms.ModelForm):
    class Meta:
        model = Enquiry
        fields = ['name', 'phone', 'email', 'company', 'product', 'product_name', 'quantity', 'unit', 'location', 'message']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Your Full Name',
                'required': True,
                'autocomplete': 'name',
                'id': 'f-name',
            }),
            'phone': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Mobile Number (e.g. +91 98765 43210)',
                'required': True,
                'autocomplete': 'tel',
                'id': 'f-mobile',
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email Address (optional)',
                'autocomplete': 'email',
                'id': 'f-email',
            }),
            'company': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Company / Contractor Firm (optional)',
                'id': 'f-company',
            }),
            'product': forms.Select(attrs={
                'class': 'form-select',
                'id': 'f-product',
            }),
            'product_name': forms.HiddenInput(),
            'quantity': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'e.g. 10',
                'id': 'f-quantity',
            }),
            'unit': forms.Select(attrs={
                'class': 'form-select',
                'id': 'f-unit',
            }, choices=[
                ('', 'Select unit'),
                ('Ton', 'Ton'),
                ('Truck', 'Truck (Full Load)'),
                ('Cubic Meter', 'Cubic Meter'),
                ('Brass', 'Brass'),
                ('Other', 'Other'),
            ]),
            'location': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'City, Project Site, or Landmark',
                'id': 'f-location',
            }),
            'message': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Tell us about your project, timeline, or special requirements...',
                'id': 'f-message',
                'required': True,
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['product'].queryset = Product.objects.all()
        self.fields['product'].required = False
        self.fields['product'].empty_label = "Select a product (or mention below)"

    def clean_phone(self):
        phone = self.cleaned_data.get('phone', '').strip()
        cleaned_phone = re.sub(r'[\s\-\(\)\.]', '', phone)
        if len(cleaned_phone) < 10 or not re.match(r'^\+?[0-9]{10,15}$', cleaned_phone):
            raise ValidationError("Please provide a valid 10-digit mobile number.")
        return phone
