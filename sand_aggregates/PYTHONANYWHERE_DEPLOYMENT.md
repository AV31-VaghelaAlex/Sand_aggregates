# Deploying Sand Aggregates on PythonAnywhere

Step-by-step walkthrough for deploying the **Sand Aggregates Management & Ordering System** (**LJ ENTERPRISE**) on [PythonAnywhere](https://www.pythonanywhere.com/).

---

## Architecture Summary

| Component | Setting on PythonAnywhere |
| :--- | :--- |
| **Python Version** | Python 3.10 |
| **Project Directory** | `/home/<username>/Sand_aggregates/sand_aggregates` |
| **Virtualenv Directory** | `/home/<username>/Sand_aggregates/sand_aggregates/venv` (or `/home/<username>/.virtualenvs/sand-venv`) |
| **Database** | SQLite (`db.sqlite3` — preserved permanently on your PythonAnywhere storage) |
| **Static Files Directory** | `/home/<username>/Sand_aggregates/sand_aggregates/staticfiles` |
| **Media Files Directory** | `/home/<username>/Sand_aggregates/sand_aggregates/media` |
| **WSGI File** | `/var/www/<username>_pythonanywhere_com_wsgi.py` |

*(Replace `<username>` everywhere with your actual PythonAnywhere username)*

---

## Step 1: Push Local Changes to GitHub

On your local development machine, commit and push the updated production settings:

```bash
git add .
git commit -m "Configure production CSRF, SSL proxy, and PythonAnywhere WSGI setup"
git push origin main
```

---

## Step 2: Open a Bash Console on PythonAnywhere

1. Log in to [PythonAnywhere](https://www.pythonanywhere.com/).
2. On your **Dashboard**, navigate to **Consoles**.
3. Under **Start a new console**, click **Bash**.

---

## Step 3: Clone the Repository & Set Up Virtual Environment

In the PythonAnywhere Bash console, run:

```bash
# 1. Clone your GitHub repository
git clone https://github.com/AV31-VaghelaAlex/Sand_aggregates.git

# 2. Enter the Django project folder
cd Sand_aggregates/sand_aggregates

# 3. Create a Python 3.10 virtual environment
python3.10 -m venv venv

# 4. Activate the virtual environment
source venv/bin/activate

# 5. Upgrade pip and install dependencies
pip install --upgrade pip
pip install -r requirements.txt
```

---

## Step 4: Configure Production Environment Variables

Still in `cd ~/Sand_aggregates/sand_aggregates` with the virtual environment activated:

```bash
# Copy the environment template
cp .env.example .env

# Edit the .env file using nano
nano .env
```

Make sure the following lines in `.env` reflect your live server:

```ini
DJANGO_DEBUG=False
DJANGO_SECRET_KEY=generate-a-strong-random-key-here
DJANGO_ALLOWED_HOSTS=<username>.pythonanywhere.com,localhost,127.0.0.1
DJANGO_CSRF_TRUSTED_ORIGINS=https://<username>.pythonanywhere.com
```

*(Press `Ctrl + O` then `Enter` to save, and `Ctrl + X` to exit nano)*

---

## Step 5: Initialize Database & Collect Static Files

Run the migration, seeding, and static collection commands:

```bash
# 1. Run migrations
python manage.py migrate

# 2. Seed default categories, products, and admin credentials
python manage.py seed_data

# 3. Collect static files for WhiteNoise and Nginx
python manage.py collectstatic --noinput
```

> **Default Admin Account created by `seed_data`**:
> - **Username**: `admin`
> - **Password**: `admin123`
> *(You can change this password after logging in at `/admin/`)*

---

## Step 6: Create & Configure the Web App in PythonAnywhere

1. In PythonAnywhere top menu, click the **Web** tab.
2. Click **Add a new web app**.
3. When prompted:
   - Domain: `<username>.pythonanywhere.com` (Click Next)
   - Select a Python Web Framework: Click **Manual configuration** (do **NOT** click "Django" here because our project is already built).
   - Select Python version: Choose **Python 3.10**.
   - Click Next to finish setup.

### A. Set Code Paths
Scroll to the **Code** section on the Web tab:
- **Source code**: `/home/<username>/Sand_aggregates/sand_aggregates`
- **Working directory**: `/home/<username>/Sand_aggregates/sand_aggregates`

### B. Set Virtual Environment Path
Scroll to the **Virtualenv** section:
- Enter: `/home/<username>/Sand_aggregates/sand_aggregates/venv`
- Click the blue checkmark.

### C. Configure WSGI File
In the **Code** section, find **WSGI configuration file**:
- Click the link `/var/www/<username>_pythonanywhere_com_wsgi.py`.
- Delete everything in that file.
- Paste the following configuration (replace `<username>` with your actual username):

```python
import os
import sys
from pathlib import Path

# Path to the Django project containing manage.py and sand_aggregates/
path = '/home/<username>/Sand_aggregates/sand_aggregates'
if path not in sys.path:
    sys.path.insert(0, path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'sand_aggregates.settings'

# Load .env variables
try:
    from dotenv import load_dotenv
    load_dotenv(os.path.join(path, '.env'))
except ImportError:
    pass

# WSGI handler
from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

- Click the green **Save** button in the top right, then return to the **Web** tab.

---

## Step 7: Configure Static & Media Files Mappings

Scroll down to the **Static files** section on the **Web** tab. Add the following two rows:

| URL | Directory |
| :--- | :--- |
| `/static/` | `/home/<username>/Sand_aggregates/sand_aggregates/staticfiles` |
| `/media/` | `/home/<username>/Sand_aggregates/sand_aggregates/media` |

---

## Step 8: Reload the Web App

Scroll back up to the top of the **Web** tab and click the large green button:
**Reload <username>.pythonanywhere.com**

Now open your browser and visit:
`https://<username>.pythonanywhere.com`

---

## Step 9: Verification Checklist

1. **Homepage**: Verify hero, trust strip, materials showcase, and logo render properly.
2. **Catalog (`/products/`)**: Verify product cards, images, and prices show up.
3. **Placing an Order (`/order/`)**: Place a test order to ensure CSRF token verification succeeds.
4. **Admin Portal (`/admin/`)**: Log in with `admin` / `admin123`.
5. **Dashboard (`/admin-dashboard/`)**: Check stat cards and Chart.js visualizations.

---

## Future Updates (Deploying Code Changes)

Whenever you push new updates to your GitHub repository:

1. Open a Bash console in PythonAnywhere.
2. Run:
```bash
cd ~/Sand_aggregates/sand_aggregates
source venv/bin/activate
git pull origin main
python manage.py migrate
python manage.py collectstatic --noinput
```
3. Go to the **Web** tab and click **Reload**.
