from datetime import datetime
import urllib.parse
from django.conf import settings
from .models import SiteSetting, Category


def site_context(request):
    """
    Context processor to provide business contact information,
    social links, categories, and pre-calculated WhatsApp links to all templates.
    """
    try:
        site_config = SiteSetting.get_settings()
    except Exception:
        # Fallback to defaults if database is not yet migrated
        class FakeSettings:
            business_name = settings.SITE_DEFAULTS.get('BUSINESS_NAME', 'Apex Sand & Aggregates')
            tagline = "Quality sand and aggregates for stronger construction"
            phone_display = settings.SITE_DEFAULTS.get('PHONE_NUMBER', '+91 98765 43210')
            phone_raw = settings.SITE_DEFAULTS.get('PHONE_RAW', '+919876543210')
            whatsapp_number = settings.SITE_DEFAULTS.get('WHATSAPP_NUMBER', '919876543210')
            email = settings.SITE_DEFAULTS.get('EMAIL_ADDRESS', 'info@apexaggregates.com')
            address = settings.SITE_DEFAULTS.get('ADDRESS', 'Highway Industrial Area, Gujarat, India')
            business_hours = settings.SITE_DEFAULTS.get('BUSINESS_HOURS', 'Mon - Sat: 8:00 AM - 7:00 PM')
            google_maps_url = settings.SITE_DEFAULTS.get('GOOGLE_MAPS_URL', '')
            whatsapp_default_message = "Hello, I am interested in your sand and aggregates products. I would like to know the price and availability."
            instagram_url = settings.SITE_DEFAULTS.get('INSTAGRAM_URL', 'https://www.instagram.com/infoljenterprise?stkn=MWd3cGN3dDV6Ym44aA==')
            linkedin_url = settings.SITE_DEFAULTS.get('LINKEDIN_URL', 'https://www.linkedin.com/company/rashienterprise')
        site_config = FakeSettings()

    # Pre-generate standard WhatsApp URL
    encoded_default_msg = urllib.parse.quote(site_config.whatsapp_default_message)
    whatsapp_url = f"https://wa.me/{site_config.whatsapp_number}?text={encoded_default_msg}"

    # Active categories for navbar or footer
    try:
        categories = Category.objects.filter(is_active=True).order_by('order', 'name')
    except Exception:
        categories = []

    return {
        'site_settings': site_config,
        'whatsapp_url': whatsapp_url,
        'nav_categories': categories,
        'current_year': datetime.now().year,
    }
