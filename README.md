 # Inventory Management System — Production Documentation

This repository contains a lightweight Inventory Management System built with FastAPI, SQLAlchemy and Jinja2 templates. It is intended as a pragmatic starter for small-to-medium inventory/e‑commerce projects and includes an admin dashboard and customer-facing storefront.

Overview
--------
- FastAPI app with a REST API (under `/api/*`) and server-rendered pages (web routes).
- SQLAlchemy ORM models with Alembic-compatible migrations.
- Jinja2 templates and Bootstrap-based frontend in `app/templates` and `app/static`.

Primary features (implemented)
------------------------------
- Products: listing, admin CRUD, price, SKU and stock
- Cart: persistent cart (add/update/remove) and checkout → `Order` creation
- Orders: list (customer) and detailed view per order
- Wishlist: add/remove favorites from product cards, user wishlist page
- Notifications: admin send/broadcast; customer inbox + mark-as-read
- Admin pages: basic `customers` management and `analytics` metrics

Working features (5–7 key, ready-to-use)
-------------------------------------
1. Product management — Full CRUD for products from the admin UI and API (`/api/products/`), including stock and SKU handling; customers view product lists at `/products`.
2. Persistent Cart & Checkout — Customers can add/update/remove cart items via `/api/carts/`, and complete checkout with `/api/carts/checkout`, which creates `Order` records and decrements stock.
3. Orders & Order Detail — Customers see their orders at `/orders` and a detailed order page at `/orders/{id}` with line items and totals.
4. Wishlist — Add/remove products to a personal wishlist from the product cards and view at `/wishlists` (API: `/api/wishlists/`).
5. Notifications — Admins can send or broadcast notifications (`/api/notifications/send`, `/api/notifications/broadcast`); users see notifications at `/notifications` and can mark as read.
6. Admin Dashboard & Customer Management — Admin UI with `/analytics` (metrics), `/customers` (list + enable/disable) and guarded admin routes enforced server-side.
7. Authentication & Role-based Access Control — JWT-based cookie auth with server-side `require_admin` / `require_authenticated` dependencies protecting APIs and web pages; admin seeded on first startup.

Architecture & Key Files
------------------------
- `app/main.py` — app entrypoint and router registration
- `app/api/` — REST API routers: `products`, `carts`, `orders`, `wishlists`, `notifications`, `customers`, etc.
- `app/web/routes.py` — server-rendered routes for HTML pages
- `app/templates/` — Jinja2 templates used by web routes
- `app/static/` — CSS and static assets
- `app/models/` — SQLAlchemy models (`Product`, `Cart`, `Order`, `Wishlist`, `Notification`, `User`, ...)
- `app/services/` & `app/repositories/` — business logic and DB access layers
- `requirements.txt` — pinned dependencies required to run the project

Dependencies
------------
Primary runtime packages (from `requirements.txt`):
- `fastapi`, `uvicorn[standard]` — web framework and server
- `sqlalchemy`, `alembic` — ORM and migrations
- `pydantic`, `pydantic-settings` — settings and data validation
- `jinja2`, `python-multipart` — templating and form parsing
- `python-jose[cryptography]`, `bcrypt`, `passlib[bcrypt]` — JWT and password hashing
- `pymysql` — MySQL driver (used for MySQL/MariaDB; optional)

Utilities and optional packages included:
- `pandas`, `numpy`, `matplotlib`, `openpyxl`, `xlsxwriter`, `reportlab` — reporting & exports
- `python-barcode`, `qrcode`, `Pillow`, `pyzbar` — barcode/Qr code and image handling
- `schedule` — lightweight task scheduling (in-process)
- `pytest`, `pytest-cov` — test tooling

Note: For Postgres use `psycopg[binary]` and set `DATABASE_URL` accordingly. Adjust `requirements.txt` if you switch DB drivers.

Environment & Configuration
---------------------------
The app reads configuration from environment variables (via `pydantic-settings`). Key variables:
- `DATABASE_URL` — SQLAlchemy database URL (e.g. `sqlite:///./dev.db`, `postgresql+psycopg2://user:pass@host/db`)
- `SECRET_KEY` — JWT signing secret (set in production)
- `ACCESS_TOKEN_EXPIRE_MINUTES` — token lifetime (integer)
- `APP_NAME` — display name for the app

Local development defaults are safe for experimentation, but set strong secrets and a production DB for deployments.

Quickstart — Linux / macOS
--------------------------
1. Clone the repo and enter it:

```bash
git clone <repo> && cd inventoryManagementSystem-
```

2. Create and activate a virtual environment:

```bash
python3 -m venv venv
source venv/bin/activate
```

3. Install dependencies:

```bash
pip install -r requirements.txt
```

4. (Optional) set an SQLite DB for development:

```bash
export DATABASE_URL=sqlite:///./dev.db
export SECRET_KEY="dev-secret"
```

5. Start the app:

```bash
uvicorn app.main:app --reload
```

6. Open `http://localhost:8000`.

The project seeds a default admin user on first startup: `admin@example.com` / `admin123` (change in production).

Quickstart — Windows (PowerShell)
---------------------------------
```powershell
git clone <repo>; cd inventoryManagementSystem-
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
$env:DATABASE_URL = 'sqlite:///./dev.db'
$env:SECRET_KEY = 'dev-secret'
uvicorn app.main:app --reload
```

Docker (optional)
-----------------
You can run the app inside a container. Example Dockerfile and docker-compose are not included by default, but a simple approach:

```dockerfile
FROM python:3.11-slim
WORKDIR /app
COPY . /app
RUN python -m pip install --upgrade pip && pip install -r requirements.txt
ENV DATABASE_URL=sqlite:///./dev.db
CMD ["uvicorn","app.main:app","--host","0.0.0.0","--port","8000"]
```

Run migrations (Alembic)
------------------------
If you use Alembic, update `alembic.ini` and run:

```bash
alembic upgrade head
```

Seed data
---------
On startup the app attempts to create an admin user if none exists. For more complex seeding, provide a `seeder.py` script or call services to create demo data.

API Summary (high level)
-------------------------
- `GET /api/products/` — list products
- `POST /api/products/` — create product (admin)
- `GET /api/products/{id}` — product detail
- `GET /api/products/search?q=` — search

- `GET /api/carts/` — current user's cart
- `POST /api/carts/add?product_id=&quantity=` — add to cart
- `PUT /api/carts/{item_id}?quantity=` — update cart item
- `DELETE /api/carts/{item_id}` — remove cart item
- `POST /api/carts/checkout` — checkout (creates order)

- `GET /api/wishlists/`, `POST /api/wishlists/add?product_id=`, `DELETE /api/wishlists/{id}`

- `GET /api/notifications/`, `PUT /api/notifications/{id}/mark-read`, `POST /api/notifications/send`, `POST /api/notifications/broadcast`

Web pages (server-rendered)
--------------------------
- `/products` — product listing (customer & admin UI)
- `/cart` — cart page
- `/wishlists` — wishlist page
- `/orders` — customer's orders
- `/orders/{id}` — order detail
- Admin pages (admin only): `/` (dashboard), `/analytics`, `/customers`, `/notifications`

Security & Production Notes
---------------------------
- Always set `SECRET_KEY` in production and rotate it appropriately.
- Use HTTPS and set `secure=True` for cookies.
- Use a robust RDBMS (Postgres, MySQL) and connection pooling.
- Run Alembic migrations during deployment and never run `Base.metadata.create_all()` in production without care.
- Validate user input at both API and UI boundaries.

Testing
-------
Run unit and integration tests with `pytest`.

```bash
pytest -q
```

Suggested integration tests:
- Cart add → checkout → order exists and product quantity decremented
- Wishlist add/remove
- Notifications sending and marking read

Roadmap / Future Work
---------------------
- Product variants & sizes (per-variant stock and SKU)
- Payment integration and order payment status
- Inventory reservations and optimistic locking for high concurrency
- Role & permission management UI (fine grained)
- Export/reporting pipelines, scheduled backups
- End-to-end tests and CI/CD pipeline

Contributing
------------
Fork and open pull requests. Follow the existing code style, add tests for new features, and update this README if you change behaviors or APIs.

License
-------
This project currently does not include a license file. Add a `LICENSE` when preparing for public distribution.

Questions / Next steps
---------------------
If you want, I can now:
- implement product variants/sizes (recommended next step to fully support size=0 availability rules),
- add automated integration tests for cart→checkout,
- or expand admin UI with pagination/search and CSV export.

Which should I do next?

