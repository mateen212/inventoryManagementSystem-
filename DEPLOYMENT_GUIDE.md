# Deployment Guide - Live Server Setup

## Prerequisites

- Python 3.8+
- pip or conda
- PostgreSQL (or SQLite for development)
- Virtual environment set up

## Initial Deployment Steps

### 1. Clone Repository
```bash
git clone <repository-url>
cd inventory_system
```

### 2. Create Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment
Create `.env` file:
```env
# Database Configuration
DATABASE_URL=postgresql://user:password@localhost/inventory_db
# or for SQLite:
# DATABASE_URL=sqlite:///./inventory.db

# Security
SECRET_KEY=your-very-secret-key-here-change-in-production
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=60

# Application
APP_NAME=Inventory Management System
DEBUG=False
```

### 5. Initialize Database
```bash
# Option A: Quick setup (init + seed in one command)
python setup_database.py

# Option B: Step by step
python init_db.py      # Creates tables and roles
python seeder.py       # Adds sample data
```

### 6. Verify Setup
```bash
# Check if database is created
ls -la inventory.db  # or check PostgreSQL

# Check roles were created
python -c "
from app.database import SessionLocal
from app.models.user import Role

db = SessionLocal()
roles = db.query(Role).all()
for role in roles:
    print(f'Role: {role.name}')
db.close()
"
```

---

## Running on Live Server

### Using Gunicorn (Recommended)

#### 1. Install Gunicorn
```bash
pip install gunicorn
```

#### 2. Create Service File
Create `/etc/systemd/system/inventory.service`:
```ini
[Unit]
Description=Inventory Management System
After=network.target

[Service]
Type=notify
User=www-data
Group=www-data
WorkingDirectory=/var/www/inventory_system
Environment="PATH=/var/www/inventory_system/venv/bin"
ExecStart=/var/www/inventory_system/venv/bin/gunicorn \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 0.0.0.0:8000 \
    app.main:app

Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

#### 3. Enable and Start Service
```bash
sudo systemctl daemon-reload
sudo systemctl enable inventory
sudo systemctl start inventory
sudo systemctl status inventory
```

#### 4. View Logs
```bash
sudo journalctl -u inventory -f
```

### Using Supervisor

#### 1. Install Supervisor
```bash
sudo apt-get install supervisor
```

#### 2. Create Config File
Create `/etc/supervisor/conf.d/inventory.conf`:
```ini
[program:inventory]
command=/var/www/inventory_system/venv/bin/gunicorn \
    --workers 4 \
    --worker-class uvicorn.workers.UvicornWorker \
    --bind 127.0.0.1:8000 \
    app.main:app
directory=/var/www/inventory_system
user=www-data
autostart=true
autorestart=true
redirect_stderr=true
stdout_logfile=/var/log/inventory/app.log
```

#### 3. Start Supervisor
```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start inventory
```

### Using Nginx as Reverse Proxy

Create `/etc/nginx/sites-available/inventory`:
```nginx
server {
    listen 80;
    server_name yourdomain.com;

    # Redirect HTTP to HTTPS
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl http2;
    server_name yourdomain.com;

    # SSL Configuration
    ssl_certificate /etc/letsencrypt/live/yourdomain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/yourdomain.com/privkey.pem;
    
    # SSL Settings
    ssl_protocols TLSv1.2 TLSv1.3;
    ssl_ciphers HIGH:!aNULL:!MD5;
    ssl_prefer_server_ciphers on;

    client_max_body_size 100M;

    location / {
        proxy_pass http://127.0.0.1:8000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_redirect off;
    }

    location /static/ {
        alias /var/www/inventory_system/app/static/;
    }
}
```

Enable site:
```bash
sudo ln -s /etc/nginx/sites-available/inventory /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx
```

---

## Database Operations

### Reset Database (Keep Structure, Clear Data)
```bash
# Delete all data but keep tables
python -c "
from app.database import SessionLocal, engine
from app.models.user import User
from app.models.product import Product
from app.models.category import Category
from app.models.supplier import Supplier

db = SessionLocal()
db.query(Product).delete()
db.query(Category).delete()
db.query(Supplier).delete()
db.query(User).delete()
db.commit()
db.close()
print('✓ Data cleared')
"

# Re-seed data
python seeder.py
```

### Backup Database

#### SQLite
```bash
cp inventory.db inventory.db.backup-$(date +%Y%m%d-%H%M%S)
```

#### PostgreSQL
```bash
pg_dump -U user inventory_db > backup-$(date +%Y%m%d-%H%M%S).sql
```

### Restore Database

#### PostgreSQL
```bash
psql -U user inventory_db < backup-2024-01-15-120000.sql
```

---

## Scheduled Tasks (Cron)

### Daily Backup
Create script `/usr/local/bin/backup_inventory.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/backups/inventory"
DATE=$(date +%Y%m%d-%H%M%S)

mkdir -p $BACKUP_DIR

# PostgreSQL backup
pg_dump -U inventory_user inventory_db > $BACKUP_DIR/inventory-$DATE.sql
gzip $BACKUP_DIR/inventory-$DATE.sql

# Keep only last 30 days of backups
find $BACKUP_DIR -name "inventory-*.sql.gz" -mtime +30 -delete

echo "✓ Backup completed: $DATE"
```

Make executable:
```bash
sudo chmod +x /usr/local/bin/backup_inventory.sh
```

Add to crontab:
```bash
sudo crontab -e
```

Add line:
```
0 2 * * * /usr/local/bin/backup_inventory.sh
```

---

## Updating on Live Server

### Update Application Code
```bash
cd /var/www/inventory_system
git pull origin main
source venv/bin/activate
pip install -r requirements.txt
```

### Update Database Schema (if needed)
```bash
# Alembic migrations (if implemented)
alembic upgrade head

# Or manually run database operations
python init_db.py  # Safe - only creates missing tables/roles
```

### Restart Service
```bash
sudo systemctl restart inventory
# or
sudo supervisorctl restart inventory
```

---

## Monitoring & Maintenance

### Check Application Status
```bash
# Systemd
sudo systemctl status inventory

# Supervisor
sudo supervisorctl status inventory

# Log viewing
sudo journalctl -u inventory -f
```

### Monitor Database
```bash
# Check database size
du -sh /var/lib/postgresql/inventory_db
# or for SQLite
du -sh inventory.db
```

### Performance Optimization

1. **Add Indexes** (if using PostgreSQL)
```sql
CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_role_id ON users(role_id);
CREATE INDEX idx_products_category_id ON products(category_id);
CREATE INDEX idx_products_supplier_id ON products(supplier_id);
```

2. **Enable Query Logging**
Edit `app/config.py`:
```python
SQLALCHEMY_ECHO = False  # Set to True in development only
```

3. **Tune Database Connection Pool**
Edit `app/database.py`:
```python
engine = create_engine(
    settings.DATABASE_URL,
    pool_size=20,
    max_overflow=40,
    pool_pre_ping=True,
)
```

---

## Security Checklist

- [ ] Change `SECRET_KEY` in `.env`
- [ ] Set `DEBUG = False` in production
- [ ] Use HTTPS with valid SSL certificate
- [ ] Change default admin password
- [ ] Set up firewall rules
- [ ] Enable database backups
- [ ] Set up log rotation
- [ ] Use strong database password
- [ ] Restrict file permissions (600 for .env)
- [ ] Enable CORS only for trusted domains
- [ ] Set up rate limiting
- [ ] Enable audit logging
- [ ] Regular security updates

---

## Troubleshooting

### Application won't start
```bash
# Check logs
sudo journalctl -u inventory -n 50
sudo tail -f /var/log/inventory/app.log

# Check port conflicts
sudo lsof -i :8000

# Test database connection
python -c "
from app.database import SessionLocal
db = SessionLocal()
print('✓ Database connected')
db.close()
"
```

### Database connection errors
```bash
# PostgreSQL connection test
psql -U inventory_user -d inventory_db -h localhost

# Check environment variables
printenv | grep DATABASE_URL
```

### High memory usage
```bash
# Check process memory
ps aux | grep gunicorn

# Reduce worker count in service file
# workers 2 (instead of 4)
```

### Slow queries
Enable query logging and use database profiler:
```python
# In app/database.py
import logging
logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.INFO)
```

---

## Production Configuration Example

```env
# .env (Production)
DATABASE_URL=postgresql://prod_user:strong_password@db.example.com/inventory_prod
SECRET_KEY=very-long-random-string-at-least-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
APP_NAME=Inventory Management System
DEBUG=False
```

---

## Health Check Endpoint

Add to `app/main.py`:
```python
@app.get("/health")
def health_check():
    return {
        "status": "healthy",
        "timestamp": datetime.utcnow().isoformat()
    }
```

Test health:
```bash
curl https://yourdomain.com/health
```

Configure Nginx to use health check:
```nginx
upstream app {
    server 127.0.0.1:8000;
    keepalive 32;
}

server {
    ...
    location / {
        proxy_pass http://app;
    }
}
```

---

## Support & Documentation

- API Documentation: `https://yourdomain.com/docs`
- RBAC Guide: `RBAC_IMPLEMENTATION.md`
- API Reference: `API_ENDPOINTS.md`
- Quick Start: `QUICK_START.md`
