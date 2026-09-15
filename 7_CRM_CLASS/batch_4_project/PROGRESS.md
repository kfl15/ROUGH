# CRM API Training Progress

## Done

- Cloned the project from GitHub.
- Inspected the Django project structure.
- Confirmed the main Django project is inside `crm/`.
- Confirmed the app name is `registration`.
- Confirmed existing models: `Registration` and `Bill`.
- Confirmed existing HTML/function-based views render correctly.
- Confirmed PostgreSQL runs in Docker as `crm-postgres`.
- Confirmed Portainer is running locally.
- Confirmed all existing migrations are applied.
- Added support files:
  - `docker-compose.yml`
  - `requirements.txt`
  - `.gitignore`
  - `README.md`
  - `PROGRESS.md`
- Tested the README setup flow with a local virtual environment.
- Confirmed `docker compose up -d` works with project name `batch_4_project`.
- Confirmed these pages return HTTP 200:
  - `/`
  - `/account/registration/`
  - `/account/customer/`
  - `/account/customer/bill`

## Current Run Notes

- Django runs locally with `python manage.py runserver`.
- PostgreSQL runs in Docker.
- The current project code expects PostgreSQL on `localhost:5432`.
- The Docker database password is `postgres`.
- Because we are not editing `crm/crm/settings.py` yet, run Django commands with:

```bash
PGPASSWORD=postgres python manage.py <command>
```

## Next Lessons

1. Understand current normal Django function-based views.
2. Learn what API and JSON mean.
3. Learn why API views are different from template views.
4. Add Django REST Framework to the project settings.
5. Create `RegistrationSerializer`.
6. Create `RegistrationViewSet`.
7. Register routes with DRF router.
8. Test Registration CRUD APIs.
9. Prepare Bill API as student assignment.

## Main Code Files Not Edited Yet

- `crm/crm/settings.py`
- `crm/crm/urls.py`
- `crm/registration/views.py`
- `crm/registration/models.py`
- Templates
