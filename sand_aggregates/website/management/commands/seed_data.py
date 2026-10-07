from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from django.conf import settings
from decimal import Decimal
from pathlib import Path
import shutil
from website.models import Category, Product, Order, Enquiry, SiteSetting

User = get_user_model()


class Command(BaseCommand):
    help = "Seed initial data: admin user, site configuration, categories, products, sample orders, and enquiries."

    def handle(self, *args, **options):
        self.stdout.write(self.style.NOTICE("Seeding Sand Aggregates initial data..."))

        # 1. Superuser
        admin_user, created = User.objects.get_or_create(
            username='admin',
            defaults={
                'email': 'admin@apexaggregates.com',
                'is_staff': True,
                'is_superuser': True,
            }
        )
        if created:
            admin_user.set_password('admin123')
            admin_user.save()
            self.stdout.write(self.style.SUCCESS("Created superuser: 'admin' with password 'admin123'"))
        else:
            self.stdout.write(self.style.WARNING("Superuser 'admin' already exists."))

        # 2. Site Configuration
        site_config, _ = SiteSetting.objects.get_or_create(pk=1)
        site_config.business_name = "LJ ENTERPRISE"
        site_config.tagline = "At the heart of every strong structure lies a solid foundation — and that starts with quality materials."
        site_config.phone_display = "+91 81413 52886"
        site_config.phone_raw = "+918141352886"
        site_config.whatsapp_number = "918141352886"
        site_config.email = "infoljenterprise07@gmail.com"
        site_config.address = "Ahmedabad, Gujarat, India"
        site_config.business_hours = "Open 24 hours"
        site_config.google_maps_url = "https://www.google.com/maps?q=Ahmedabad,Gujarat,India&output=embed"
        site_config.instagram_url = "https://www.instagram.com/infoljenterprise?stkn=MWd3cGN3dDV6Ym44aA=="
        site_config.linkedin_url = "https://www.linkedin.com/company/rashienterprise"
        site_config.save()
        self.stdout.write(self.style.SUCCESS("Configured Site Settings."))

        # 3. Categories
        cat_sand, _ = Category.objects.get_or_create(
            slug='sand-fine-aggregates',
            defaults={'name': 'Sand & Fine Aggregates', 'order': 1, 'description': 'Natural river sand, manufactured sand (M-Sand), and plaster sand.'}
        )
        cat_stone, _ = Category.objects.get_or_create(
            slug='coarse-stone-aggregates',
            defaults={'name': 'Coarse Stone Aggregates', 'order': 2, 'description': 'Crushed blue metal stone aggregates in 10mm, 20mm sizes for concrete.'}
        )

        # 4. Product Media Initialization
        media_products_dir = settings.MEDIA_ROOT / 'products'
        media_products_dir.mkdir(parents=True, exist_ok=True)
        static_images_dir = settings.BASE_DIR / 'static' / 'images'
        if static_images_dir.exists():
            for img_file in static_images_dir.glob('*.*'):
                dest_file = media_products_dir / img_file.name
                if not dest_file.exists():
                    shutil.copy2(img_file, dest_file)
            self.stdout.write(self.style.SUCCESS("Initialized media/products assets."))

        # 5. Products
        products_data = [
            {
                'name': 'Coarse Sand',
                'category': cat_sand,
                'image': 'products/coarse-sand.jpg',
                'short_description': 'Stronger Concrete, Better Binding. Ideal for structural RCC.',
                'description': 'Superior quality coarse sand suitable for concrete reinforcement, structural RCC slabs, foundation columns, and high-strength load bearing members.',
                'price': Decimal('1350.00'),
                'unit': 'Ton',
                'featured': True,
                'available': True,
            },
            {
                'name': 'Banas Sand',
                'category': cat_sand,
                'image': 'products/banas-sand.jpg',
                'short_description': 'High Quality, Maximum Strength. Natural river sand.',
                'description': 'Authentic Banas river sand sourced from premium riverbeds. Free of excessive clay and silt, widely acknowledged for superior bonding and compressive strength.',
                'price': Decimal('1700.00'),
                'unit': 'Ton',
                'featured': True,
                'available': True,
            },
            {
                'name': 'M-Sand',
                'category': cat_sand,
                'image': 'products/msand.jpg',
                'short_description': 'Manufactured sand engineered for superior concrete strength.',
                'description': 'Crushed manufactured sand produced via VSI (Vertical Shaft Impactor) machines with cubic grain shape. An eco-friendly and economical replacement for river sand with zero wastage.',
                'price': Decimal('1100.00'),
                'unit': 'Ton',
                'featured': True,
                'available': True,
            },
            {
                'name': 'Fine Sand',
                'category': cat_sand,
                'image': 'products/fine-sand.jpg',
                'short_description': 'Best for Plastering & Brickwork. Clean and silt-screened.',
                'description': 'Fine mesh graded sand specially screened for internal and external wall plastering, joint mortar, bricklaying, and tile bedding.',
                'price': Decimal('1250.00'),
                'unit': 'Ton',
                'featured': True,
                'available': True,
            },
            {
                'name': '10mm Aggregate',
                'category': cat_stone,
                'image': 'products/aggregate-10mm.jpg',
                'short_description': 'Crushed stone aggregate for precast items, columns, and RCC roofing.',
                'description': 'Single-sized 10mm blue metal granite crushed aggregate. Essential for dense reinforcement concrete, precast slabs, pipe casting, and beam manufacturing.',
                'price': Decimal('1350.00'),
                'unit': 'Ton',
                'featured': True,
                'available': True,
            },
            {
                'name': '20mm Aggregate',
                'category': cat_stone,
                'image': 'products/aggregate-20mm.jpg',
                'short_description': 'Standard crushed aggregate for RCC structures, slabs, and foundations.',
                'description': 'The most widely used aggregate in all structural civil engineering. Tested for flakiness and elongation index under strict IS specifications. Delivers high compressive load capacity.',
                'price': Decimal('1450.00'),
                'unit': 'Ton',
                'featured': True,
                'available': True,
            },
        ]

        for p_data in products_data:
            p, created = Product.objects.get_or_create(
                name=p_data['name'],
                defaults=p_data
            )
            if created:
                self.stdout.write(f"Created product: {p.name}")

        # 5. Sample Orders (if none exist)
        if not Order.objects.exists():
            p20 = Product.objects.filter(name='20mm Aggregate').first()
            p_coarse = Product.objects.filter(name='Coarse Sand').first()
            if p20:
                Order.objects.create(
                    customer_name='Rajesh Patel',
                    email='rajesh.builder@example.com',
                    phone='+91 98250 12345',
                    address='Plot 12, Green City Villa Project, Near Ring Road',
                    product=p20,
                    quantity=Decimal('25.00'),
                    notes='Need morning delivery before 10 AM by 10-wheeler dumper.',
                    status='Confirmed'
                )
            if p_coarse:
                Order.objects.create(
                    customer_name='Amit Sharma',
                    email='amit.infra@example.com',
                    phone='+91 98980 54321',
                    address='Highway Bridge Site, Survey 44, Express Corridor',
                    product=p_coarse,
                    quantity=Decimal('40.00'),
                    notes='Please supply with lab test certificate.',
                    status='Processing'
                )
            self.stdout.write(self.style.SUCCESS("Created sample orders."))

        # 6. Sample Enquiries (if none exist)
        if not Enquiry.objects.exists():
            msand = Product.objects.filter(name='M-Sand').first()
            Enquiry.objects.create(
                name='Vikram Singh',
                email='vikram@vinfra.com',
                phone='+91 97123 98765',
                company='V-Infra Projects Ltd.',
                product=msand,
                quantity='100',
                unit='Ton',
                location='Ahmedabad Highway Extension',
                message='Looking for bulk supply of M-Sand for a 6-month highway overpass project. Please share best commercial quotes.',
                status='New'
            )
            self.stdout.write(self.style.SUCCESS("Created sample enquiries."))

        self.stdout.write(self.style.SUCCESS("Database seeding completed successfully!"))
