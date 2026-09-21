# Sand Aggregates Management & Ordering System

A production-grade Django web application for construction sand, river sand, M-Sand, crushed stone aggregates, and road sub-base (GSB) supply operations.

Built by converting the static "Sand Aggregates Website" into a dynamic database-driven business platform while strictly preserving the industrial design aesthetic, colors, typography, and responsive animations.

---

## 1. Project Overview

The **Sand Aggregates Management & Ordering System** bridges quarry suppliers and construction buyers (builders, civil contractors, RMC plants, infrastructure developers). It provides an intuitive public ordering interface for clients and a full-featured management portal for administrators.

---

## 2. Features

- **Dynamic Homepage**: High-impact industrial hero section, trust highlight strip, company background, live featured materials showcase, reasons to choose us, customer segments, call-to-action banner, Google Maps location embed, and quotation request form.
- **Product & Material Catalog (`/products/`)**: Categorized material listings, keyword search filter, real-time stock availability badges, pricing per unit (Ton/Truck/m³), and instant order/enquiry triggers.
- **Detailed Material Pages (`/products/<slug>/`)**: High-resolution photography, grain grading details, structural applications, recommended material cross-sells, and pre-formatted WhatsApp enquiry generators.
- **Direct Material Ordering System (`/order/`)**:
  - Live client-side price & total cost computation (`Unit Price × Quantity = Total Amount`).
  - No mandatory upfront payment gateway required (designed for B2B cash/RTGS on-site weighbridge verification).
  - Generates unique order reference IDs (e.g. `ORD-2026-0001`).
  - Professional order summary slip with a one-click WhatsApp dispatch follow-up button.
- **Quotation & Enquiry Engine (`/enquiry/`)**: Capture inquiries with project location, company name, required tonnage, and custom technical requirements.
- **Configurable WhatsApp Integration**:
  - Click-to-chat triggers with automatic message pre-population across products, orders, and quotation forms.
  - Persistent floating WhatsApp contact button at the bottom-right corner.
  - Configurable phone number via Django Admin or environment variables.
- **Operational Admin Dashboard (`/admin-dashboard/`)**:
  - Stat cards: Total Products, Available Products, Total Orders, Pending Orders, Delivered Orders, and Gross Order Value.
  - Interactive **Chart.js** visual breakdowns for Order Status and Enquiry distribution.
  - Recent activity tables for fast dispatch workflows.
- **Django Admin Customization**:
  - In-line status updating for orders and inquiries.
  - Image thumbnails and quick-edit checkboxes for product prices, availability, and featured status.
  - Singleton `SiteSetting` model to modify phone numbers, address, social media links, and WhatsApp settings without modifying code.
- **Production Readiness**:
  - Environment variable isolation (`.env` & `.env.example`).
  - WhiteNoise configured for serving compressed static files in production.
  - Secure CSRF handling and robust form input validation.

---

## 3. Technologies

- **Backend**: Python 3.10+ / Python 3.14, Django 4.2 LTS
- **Database**: SQLite (Development) / PostgreSQL or MySQL ready (Production)
- **Frontend**: HTML5, Vanilla CSS3 (Archivo & Inter typography, charcoal `#22252A`, sand `#CDAE83`, accent `#C05621`), Bootstrap 5 utilities
- **Icons & Graphics**: Font Awesome 6, Chart.js
- **Static Assets & Serving**: WhiteNoise
- **Image Processing**: Pillow (PIL)

---

## 4. Folder Structure

```
sand_aggregates/
│
├── manage.py                         # Django administrative utility
├── requirements.txt                  # Python dependencies
├── .env.example                      # Production environment template
├── .env                              # Active environment variables
├── setup_assets.py                   # Automated sample image and texture generator
│
├── sand_aggregates/                  # Project configuration
│   ├── __init__.py
│   ├── settings.py                   # Settings with .env & WhiteNoise
│   ├── urls.py                       # Root URL routes & media handler
│   ├── wsgi.py                       # WSGI entrypoint for Gunicorn/uWSGI
│   └── asgi.py                       # ASGI entrypoint
│
├── website/                          # Core business application
│   ├── migrations/                   # Database migrations
│   ├── management/
│   │   └── commands/
│   │       ├── __init__.py
│   │       └── seed_data.py          # Initial admin, products & sample orders seeder
│   ├── __init__.py
│   ├── admin.py                      # Custom Django Admin configuration
│   ├── apps.py                       # App configuration
│   ├── models.py                     # Category, Product, Order, Enquiry, SiteSetting
│   ├── forms.py                      # OrderForm & EnquiryForm with validations
│   ├── urls.py                       # App URL endpoints
│   ├── views.py                      # Home, Catalog, Detail, Order, Dashboard views
│   ├── context_processors.py         # Global site settings & WhatsApp links
│   └── tests.py                      # Automated test suite
│
├── templates/                        # HTML templates (Django Template Language)
│   ├── base.html                     # Base layout, navbar, footer & WhatsApp float
│   ├── home.html                     # Converted dynamic homepage
│   ├── products.html                 # Material catalog with search & filters
│   ├── product_detail.html           # Material specifications & actions
│   ├── order.html                    # Order placement form with live calculator
│   ├── order_success.html            # Order receipt slip & WhatsApp button
│   ├── enquiry.html                  # Standalone quotation request form
│   ├── enquiry_success.html          # Enquiry confirmation notice
│   └── admin_dashboard.html          # Executive dashboard with Chart.js
│
├── static/                           # Static assets
│   ├── css/
│   │   └── style.css                 # Preserved & enhanced stylesheets
│   ├── js/
│   │   └── script.js                 # Preserved & enhanced interactive scripts
│   ├── images/                       # Product photos & backgrounds
│   └── assets/                       # Brand logo & hero banners
│
└── media/                            # User-uploaded files
    └── products/                     # Product photos uploaded via Admin
```

---

## 5. Installation & Setup

### Step 1: Navigate to the project directory
```bash
cd "d:/Charust university/Project/sand/sand_aggregates"
```

### Step 2: Create and activate a Virtual Environment
```bash
# Windows (PowerShell)
python -m venv venv
.\venv\Scripts\Activate.ps1

# Linux / macOS
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

---

## 6. Database Migration & Asset Setup

### Step 4: Run Database Migrations
```bash
python manage.py makemigrations website
python manage.py migrate
```

### Step 5: Setup Sample Images & Product Textures
```bash
python setup_assets.py
```

### Step 6: Seed Initial Products, Categories & Admin Superuser
Run the built-in seeder command:
```bash
python manage.py seed_data
```

This creates:
- **Default Superuser**: `admin` / `admin123`
- **Material Categories**: Sand & Fine Aggregates, Coarse Stone Aggregates, Sub-Base & Road Materials
- **Products**: Construction Sand, River Sand, M-Sand, 10mm, 20mm, 40mm Aggregates, GSB
- **Sample Orders & Enquiries**

---

## 7. Running the Application

### Development Server
```bash
python manage.py runserver
```
Access the application at:
- **Public Website**: [http://127.0.0.1:8000/](http://127.0.0.1:8000/)
- **Product Catalog**: [http://127.0.0.1:8000/products/](http://127.0.0.1:8000/products/)
- **Place Order**: [http://127.0.0.1:8000/order/](http://127.0.0.1:8000/order/)
- **Operations Dashboard**: [http://127.0.0.1:8000/admin-dashboard/](http://127.0.0.1:8000/admin-dashboard/)
- **Django Admin**: [http://127.0.0.1:8000/admin/](http://127.0.0.1:8000/admin/)

---

## 8. Admin Credentials & Management

- **Username**: `admin`
- **Password**: `admin123`

### Adding & Editing Products
1. Navigate to `/admin/website/product/`
2. Click **Add Product**
3. Specify Name, Category, Price, Unit (Ton/Truck/m³), Description, and upload an image.
4. Check **Available** or **Featured** as needed.

### Managing Site Configuration (WhatsApp, Phone, Address, Socials)
1. Go to `/admin/website/sitesetting/`
2. Modify phone numbers, WhatsApp digits, business hours, or Google Maps embed URL.
3. Save — changes reflect instantly across the entire public website.

---

## 9. Running Tests
Verify system integrity by running the test suite:
```bash
python manage.py test website
```

---

## 10. Live Server Deployment Guide (Production)

### 1. Configure `.env`
Ensure in your live server `.env` file:
```ini
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=your-long-secure-random-key-here
DJANGO_ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
```

### 2. Collect Static Files
WhiteNoise will serve compressed static assets directly:
```bash
python manage.py collectstatic --noinput
```

### 3. Run with Gunicorn (Linux/VPS)
```bash
gunicorn sand_aggregates.wsgi:application --bind 0.0.0.0:8000 --workers 3
```

---

## 11. Future Enhancements

- Customer login portal for viewing previous order invoices and dispatch status.
- SMS / WhatsApp automated dispatch notification webhook integration.
- Weighbridge slip PDF download generator.
- Multi-quarry location inventory selector.
