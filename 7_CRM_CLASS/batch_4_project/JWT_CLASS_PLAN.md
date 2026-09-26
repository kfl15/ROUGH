# Class 3 Plan: JWT Login for the Django CRM

## Purpose

Teach JWT authentication by connecting every concept directly to this existing CRM project.

The teacher will type all main project code. The assistant should explain one small step, wait for the teacher to complete it, and then check it.

Do not directly edit these files unless the teacher explicitly asks:

- `crm/crm/settings.py`
- `crm/registration/models.py`
- `crm/registration/serializers.py`
- `crm/registration/views.py`
- `crm/registration/urls.py`
- `crm/templates/login.html`

## Project Location

```text
/data/2026/7_CRM_CLASS/batch_4_project
```

Django folder:

```text
/data/2026/7_CRM_CLASS/batch_4_project/crm
```

## Current Project Situation

- PostgreSQL runs with Docker Compose.
- Django runs locally inside `.venv`.
- DRF is already installed and active.
- Registration CRUD API already works.
- Registration API URL:

```text
http://127.0.0.1:8001/account/api/registrations/
```

- Existing login URL:

```text
http://127.0.0.1:8001/account/login/
```

- The existing `login` view only displays `login.html` for a GET request.
- It does not check email/password yet.
- `Registration` is a custom CRM model, not Django's authentication `User` model.
- Registration passwords are currently stored and returned as plain text. This must not be treated as production-safe authentication.

## Simple JWT Architecture

```text
Email + password
-> Login API checks the Django User
-> Server returns access + refresh tokens
-> Client sends access token with protected requests
-> Server verifies token
-> Request is allowed or rejected
```

### Access Token

- Short lifetime.
- Sent with protected API requests.
- Header format:

```text
Authorization: Bearer <access_token>
```

### Refresh Token

- Longer lifetime.
- Used to request a new access token.
- It is not used directly to open protected APIs.

### Important Meaning

- JWT is signed so changes can be detected.
- JWT is not normally encrypted.
- Never put passwords or private information inside a token.

## Recommended Project Architecture

Use Django's built-in `User` model for login/authentication.

Keep `Registration` as CRM/customer information.

Reason:

- Django `User` already supports secure password hashing.
- SimpleJWT is designed to authenticate Django users.
- This avoids inventing unsafe authentication logic around the current plain-text Registration password.

For the first classroom demo, create one Django user whose username is the same as the email address. Later, Registration signup can also create/link a Django user.

## Planned API URLs

```text
POST /account/api/login/          -> check credentials and return tokens
POST /account/api/token/refresh/  -> create a new access token
GET  /account/api/profile/        -> protected test endpoint
```

Later, the Registration API can also be protected.

## Step-by-Step Work

### Step 1: Activate the Virtual Environment

From the project root:

```bash
cd /data/2026/7_CRM_CLASS/batch_4_project
source .venv/bin/activate
```

### Step 2: Install SimpleJWT

Completed on 2026-09-26:

```text
djangorestframework-simplejwt 5.5.1
```

The package was installed inside `.venv`.

Still required later: add this exact package/version to `requirements.txt`:

```text
djangorestframework-simplejwt==5.5.1
```

### Step 3: Check Compatibility

Current next step:

```bash
cd /data/2026/7_CRM_CLASS/batch_4_project/crm
python manage.py check
```

Why:

> Confirm that the installed package and current Django project load without errors.

Note: this project declares Django 6.1 and DRF 3.18.1. These are newer than the versions listed in the SimpleJWT 5.5.1 documentation, so testing is important.

### Step 4: Start PostgreSQL and Create a Demo Django User

From the project root:

```bash
docker compose up -d
cd crm
python manage.py createsuperuser
```

Use an email address as the username for the simple classroom demo.

### Step 5: Configure JWT Authentication

File:

```text
crm/crm/settings.py
```

Add DRF's JWT authentication class. Explain every setting before the teacher types it.

### Step 6: Create the Login Serializer

File:

```text
crm/registration/serializers.py
```

Create a small `LoginSerializer` that:

- accepts `email` and `password`;
- asks Django to authenticate the user;
- rejects incorrect credentials;
- returns access and refresh tokens.

Teaching connection:

```text
Serializer receives credentials
-> validates them
-> produces token response data
```

### Step 7: Create the Login API View

File:

```text
crm/registration/views.py
```

Create a small DRF API view that uses `LoginSerializer`.

Teaching connection:

```text
View receives POST request
-> Serializer checks credentials
-> View returns JSON tokens
```

### Step 8: Add JWT URLs

File:

```text
crm/registration/urls.py
```

Add:

- login API URL;
- refresh-token URL;
- protected profile URL.

### Step 9: Test Login

Send email and password:

```json
{
  "email": "teacher@example.com",
  "password": "the-demo-password"
}
```

Expected response shape:

```json
{
  "refresh": "...",
  "access": "..."
}
```

Do not place real passwords or complete tokens in documentation or Git.

### Step 10: Test a Protected API

Send:

```text
Authorization: Bearer <access_token>
```

Expected behavior:

- No token: `401 Unauthorized`
- Valid access token: `200 OK`
- Invalid/expired token: `401 Unauthorized`

### Step 11: Test Token Refresh

Send the refresh token to:

```text
/account/api/token/refresh/
```

Expected result: a new access token.

### Step 12: Connect `login.html`

Do this only after the API works.

The page will:

```text
collect email/password
-> send POST request to login API
-> receive tokens
-> use the access token for protected API calls
```

Token storage must be explained carefully. Browser local storage is easy for a classroom demonstration but is not the safest production design. Secure HTTP-only cookies require a different setup.

## Classroom Order

1. Show the existing login page.
2. Explain access and refresh tokens using the project flow.
3. Build the login serializer.
4. Build the login API view.
5. Add URLs.
6. Log in and receive tokens.
7. Call one protected endpoint without a token.
8. Call it again with `Bearer <access_token>`.
9. Refresh the access token.
10. Connect the HTML page only if class time remains.

## Short Mental Model

```text
Serializer -> checks login input
View       -> controls the login request
SimpleJWT  -> creates and verifies tokens
Permission -> blocks requests without valid authentication
```

## Current Resume Point

JWT implementation was completed and tested on 2026-09-26.

Completed:

- SimpleJWT installed and added to `requirements.txt`.
- JWT authentication configured in `settings.py`.
- Django demo user created.
- `LoginSerializer` validates email/password and creates tokens.
- `LoginAPIView` returns access and refresh tokens.
- Refresh-token endpoint works.
- Protected Profile API returns `401` without a token and `200` with a token.
- Registration ViewSet requires authentication.
- Existing `login.html` sends JSON to the login API.
- Browser stores both tokens and uses the access token to call Profile API.
- Django system check passes.

Class 3 slides:

```text
slides/class-3-jwt-authentication.pdf
slides/class-3-jwt-authentication.html
```
