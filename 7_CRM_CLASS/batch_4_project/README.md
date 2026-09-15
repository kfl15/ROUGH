# Django CRM Training Project

This repo is for learning an existing Django CRM project, then converting the existing `Registration` module into APIs using Django REST Framework.

Important training rule: do not edit the main Django code until you understand why the change is needed.

## Project Structure

```text
batch_4_project/
├── docker-compose.yml
├── requirements.txt
├── PROGRESS.md
└── crm/
    ├── manage.py
    ├── crm/
    │   ├── settings.py
    │   └── urls.py
    ├── registration/
    │   ├── models.py
    │   ├── views.py
    │   └── urls.py
    └── templates/
```

## What Runs Where

- PostgreSQL runs in Docker.
- Django runs locally with `python manage.py runserver`.
- Portainer can be used to see/manage the PostgreSQL container.

## 1. Clone The Project

```bash
git clone https://github.com/Salman13201016/batch_4_project.git
cd batch_4_project
```

## 2. Create Python Environment

Recommended:

```bash
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If Ubuntu says `ensurepip is not available`, install venv support first:

```bash
sudo apt install -y python3.12-venv
```

Then run the venv commands again.

Alternative on this machine, because `uv` is installed:

```bash
uv venv .venv --seed --python python3.12
source .venv/bin/activate
python -m pip install -r requirements.txt
```

## 3. Start PostgreSQL With Docker

From the repo root:

```bash
docker compose up -d
docker compose ps
```

Expected container:

```text
crm-postgres
```

Database settings used by Docker:

```text
Database: crm_batch_4
User: postgres
Password: postgres
Host: localhost
Port: 5432
```

Portainer:

```text
https://127.0.0.1:9443
```

## 4. Run Django Checks And Migrations

Go inside the Django project folder:

```bash
cd crm
```

Run Django check:

```bash
PGPASSWORD=postgres python manage.py check
```

Run migrations:

```bash
PGPASSWORD=postgres python manage.py migrate
```

Why `PGPASSWORD=postgres`?

The current `crm/crm/settings.py` has PostgreSQL password empty. We are not editing `settings.py` yet, so this command supplies the password only for the current terminal command.

## 5. Run The Django Server

Portainer uses port `8000` on this machine, so run Django on `8001`:

```bash
PGPASSWORD=postgres python manage.py runserver 127.0.0.1:8001
```

Open:

```text
http://127.0.0.1:8001/
http://127.0.0.1:8001/account/registration/
http://127.0.0.1:8001/account/customer/
http://127.0.0.1:8001/account/customer/bill
```

## 6. Current Normal Django URLs

Main URL file:

```text
crm/crm/urls.py
```

Registration app URL file:

```text
crm/registration/urls.py
```

Important existing routes:

```text
/account/registration/      signup form
/account/customer/          customer list
/account/customer/edit/<id> edit customer
/account/customer/delete/<id> delete customer
/account/customer/bill      bill form
```

## 7. Current Normal Django Flow

Current views live here:

```text
crm/registration/views.py
```

Normal Django HTML view flow:

```text
Browser form -> Django URL -> function view -> model/database -> template/redirect/HttpResponse
```

Example:

```text
GET /account/registration/
```

shows `signup.html`.

```text
POST /account/registration/
```

reads form data, creates a `Registration` object, saves it, then redirects to the customer list.

## 8. Later API Target

We will convert Registration into API endpoints:

```text
GET    /registrations/
POST   /registrations/
GET    /registrations/<id>/
PATCH  /registrations/<id>/
DELETE /registrations/<id>/
```

DRF files we will add later:

```text
crm/registration/serializers.py
```

Main files we will later edit after explanation:

```text
crm/crm/settings.py
crm/crm/urls.py
crm/registration/views.py
```

## 9. Quick Troubleshooting

If port `8000` is busy:

```bash
PGPASSWORD=postgres python manage.py runserver 127.0.0.1:8001
```

If PostgreSQL is not running:

```bash
docker compose up -d
```

If database connection fails, confirm Docker is running:

```bash
docker ps
```

You should see `crm-postgres`.
