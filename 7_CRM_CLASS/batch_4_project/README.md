# Django CRM classroom project

This repository contains the Django CRM used in class, its Registration search API, and the HTML/PDF lessons. Django runs on your computer; PostgreSQL runs in Docker.

## Run a fresh clone

You need Python 3.12 or newer, Docker with Compose, and a free local port `5432` for PostgreSQL.

```bash
git clone https://github.com/kfl15/ROUGH.git
cd ROUGH/7_CRM_CLASS/batch_4_project
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements.txt
docker compose up -d db
docker compose ps
cd crm
python manage.py migrate
python manage.py loaddata registration_search_demo
python manage.py createsuperuser
python manage.py runserver 127.0.0.1:8001
```

The fixture is optional, but it gives a **fresh database** nine fictional customers matching the examples in the search lesson. Do not load it into a database that already has customer records with the same IDs or emails. When `createsuperuser` asks for an email, enter one: the API login uses that email and the password you choose. Django User accounts and Registration customers are separate.

Open `http://127.0.0.1:8001/account/customer/` for the HTML customer list. Open `http://127.0.0.1:8001/account/api/registrations/` to see the API route; a browser request without a JWT returns `401 Unauthorized`, as expected.

To stop the server, press `Ctrl+C`. To stop PostgreSQL without deleting its data, run `docker compose down` from the project root.

## Try the API with Postman

Create two requests in one Postman collection.

**1. Login:** `POST http://127.0.0.1:8001/account/api/login/` with Body → raw → JSON:

```json
{"email":"<your Django user email>","password":"<your password>"}
```

A successful response is `200 OK` and includes `access` and `refresh` tokens. In Scripts → Post-response, save the access token:

```javascript
if (pm.response.code === 200) {
    pm.collectionVariables.set("access_token", pm.response.json().access);
}
```

**2. Registration list/search:** `GET http://127.0.0.1:8001/account/api/registrations/`. In Authorization choose **Bearer Token** and put `{{access_token}}` in the Token field. Send login first, then this request. Send login again when the short-lived access token expires.

The same GET endpoint accepts these Params:

| Param | Example | Meaning |
|---|---|---|
| `search` | `Teacher` | Partial, case-insensitive name or email search |
| `email` | `teacher.test@example.com` | Whole email match, case-insensitive |
| `dob_from` | `2026-09-01` | Date of birth on or after this date |
| `dob_to` | `2026-09-30` | Date of birth on or before this date |
| `ordering` | `-id` | Descending ID order |
| `page_size` | `3` | Records per page, up to 50 |
| `page` | `2` | Page number |

With the optional fixture, the list has `count: 9`, `?search=Teacher` has `count: 1`, the September 2026 DOB range has `count: 3`, and `?search=testcase&dob_from=2026-09-01&dob_to=2026-09-30` has `count: 1`. Counts will differ if you add or delete customers. Bad date inputs return `400`; a missing token returns `401`.

The full teacher walkthrough and expected JSON are in [Registration Search API slides](slides/registration-search-implementation.html), [PDF](slides/registration-search-implementation.pdf), and the [Markdown source](slides/REGISTRATION_SEARCH_IMPLEMENTATION_DRAFT.md).

## Project notes

- The Registration API routes are created in `crm/registration/urls.py`. Search and filters are in `crm/registration/views.py`; response fields are in `crm/registration/serializers.py`.
- The HTML customer search input is not yet connected to the API.
- The optional fixture's `Registration.password` values are fictional. This training model still stores customer passwords as plain text; do not enter real customer passwords or use that field to authenticate users. Django User authentication is separate and hashes passwords.
- Email is printed in the Django server terminal by default, so the Bill OTP demo can run without SMTP credentials. To send real email from the configured mailbox, set `EMAIL_HOST_PASSWORD` in the server environment. Set `DJANGO_SECRET_KEY` to a private value for any deployment; the default key is for local classroom use only.
- This is a development project. `DEBUG` is enabled and Django's `runserver` is not a production server.
