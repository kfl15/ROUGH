# Class Notes: Django Registration API

## 1. What Is DRF?

DRF means **Django REST Framework**.

It is a package/library that helps Django create APIs easily.

Normal Django gives HTML pages:

```text
/account/customer/  -> HTML page
```

DRF helps Django give JSON data:

```text
/account/api/registrations/  -> JSON data
```

In this project, DRF gives us:

- Serializer
  - Converts model data to JSON and if JSON formated data comes, it actually validates that.
- ViewSet (The main controler)
  - Gives API actions like list, create, retrieve, update, and delete. Uses serializer to validate data, uses router to converts action to api urls
- Router
  - Creates API URLs automatically from the ViewSet.
- Browsable API page
  - Lets us test the API from the browser without Postman.

Simple line for class:

> DRF is a Django tool that helps us build APIs instead of only HTML pages.

## Code Connection: Where These Things Are In Our Project

Use this section to connect theory with the real code.

DRF installed:

```text
crm/crm/settings.py lines 40-49
```

Work:

> `rest_framework` activates DRF inside this Django project.

Serializer:

```text
crm/registration/serializers.py lines 1-13
```

Work:

> `RegistrationSerializer` converts `Registration` model data to JSON and JSON back to model data.

ViewSet imports:

```text
crm/registration/views.py lines 9-10
```

Work:

> These lines import DRF `viewsets` and our `RegistrationSerializer`.

Registration ViewSet:

```text
crm/registration/views.py lines 126-128
```

Work:

> `RegistrationViewSet` creates the API logic using `ModelViewSet`.

Router setup:

```text
crm/registration/urls.py lines 23-27
```

Work:

> Router connects `registrations` API URL with `RegistrationViewSet`.

API URL include:

```text
crm/registration/urls.py line 36
```

Work:

> This line adds router-generated API URLs under `/account/api/`.

Browser test URL:

```text
http://127.0.0.1:8001/account/api/registrations/
```

Work:

> This URL shows the Registration API list in DRF browsable API.

Note:

> These line numbers match the current code. If code is edited later, line numbers may move.

## 2. What Is CRUD?

CRUD means:

```text
C = Create
R = Read
U = Update
D = Delete
```

These are the main actions for database data.

In our Registration API:

```text
Create -> add new registration
Read   -> see registration data
Update -> change registration data
Delete -> remove registration data
```

API URLs:

```text
GET     /account/api/registrations/       -> Read all
POST    /account/api/registrations/       -> Create new
GET     /account/api/registrations/5/     -> Read one
PUT     /account/api/registrations/5/     -> Update one
PATCH   /account/api/registrations/5/     -> Update part of one
DELETE  /account/api/registrations/5/     -> Delete one
```

Simple line for class:

> CRUD means the basic database operations: create, read, update, delete.

## 3. What Is API?

API means **Application Programming Interface**.

Easy meaning:

> API is a way for one software to talk to another software.

Normal website:

```text
Browser asks Django for page.
Django returns HTML.
Human reads the page.
```

API:

```text
Browser/mobile app/Postman asks Django for data.
Django returns JSON.
Software reads the data.
```

Example JSON:

```json
{
  "id": 5,
  "name": "testcase 4",
  "email": "testcase4@gmail.com",
  "password": "12345",
  "date_of_birth": "1996-12-12"
}
```

Simple line for class:

> API gives data, usually JSON, so another app can use it.

## 4. What Is JSON?

JSON is a simple data format.

It looks like Python dictionary, but it is used for data exchange.

Example:

```json
{
  "name": "Teacher Test",
  "email": "teacher.test@example.com"
}
```

Simple line for class:

> JSON is the common language APIs use to send and receive data.

## 5. What Is REST API?

REST API means an API that uses normal HTTP methods properly.

Main HTTP methods:

```text
GET     -> read data
POST    -> create data
PUT     -> update full data
PATCH   -> update partial data
DELETE  -> delete data
```

In our project:

```text
/account/api/registrations/
```

is a REST-style API endpoint.

Simple line for class:

> REST API means using URLs and HTTP methods to work with data.

## 6. What Is REST Framework?

In our class, REST Framework means **Django REST Framework**.

Django can build APIs manually, but DRF makes it easier.

Without DRF, we would write many views manually.

With DRF:

```text
Serializer + ViewSet + Router
```

can create CRUD API quickly.

Simple line for class:

> DRF is the helper library that makes REST APIs easier in Django.

## 7. What Did We Actually Do In This Project?

Before:

```text
Registration worked as HTML form.
User fills form.
Django saves data.
Django redirects to customer page.
```

Old flow:

```text
HTML form -> Django view -> Registration model -> PostgreSQL -> HTML page
```

After:

```text
Registration also works as API.
User/app sends JSON/form data.
DRF saves data.
DRF returns JSON response.
```

New API flow:

```text
API request -> ViewSet -> Serializer -> Registration model -> PostgreSQL -> JSON response
```

Files changed/added:

```text
crm/crm/settings.py
```

Added:

```python
'rest_framework',
```

Meaning:

> Django now knows DRF is installed and active.

```text
crm/registration/serializers.py
```

Added `RegistrationSerializer`.

Meaning:

> This decides which Registration fields become JSON.

```text
crm/registration/views.py
```

Added `RegistrationViewSet`.

Meaning:

> This gives CRUD API logic for Registration.

```text
crm/registration/urls.py
```

Added DRF router.

Meaning:

> Router automatically creates API URLs.

## 8. What Is Serializer?

Serializer is a converter.

It converts:

```text
Model object -> JSON
JSON -> Model object
```

In this project:

```python
class RegistrationSerializer(serializers.ModelSerializer):
```

means:

> Convert Registration model data to/from JSON.

Fields:

```python
fields = ['id', 'name', 'email', 'password', 'date_of_birth']
```

Meaning:

> These fields will be visible/usable in the API.

Simple line for class:

> Serializer decides what data goes in and out of the API.

## 9. What Is ViewSet?

ViewSet is API logic in one class.

In this project:

```python
class RegistrationViewSet(viewsets.ModelViewSet):
    queryset = Registration.objects.all()
    serializer_class = RegistrationSerializer
```

Meaning:

```text
queryset -> which data to use
serializer_class -> how to convert that data
```

`ModelViewSet` automatically gives:

```text
list
create
retrieve
update
delete
```

Simple line for class:

> ViewSet says which data API will work with and which serializer will handle it.

## 10. What Is Router?

Router creates API URLs automatically.

In this project:

```python
router = DefaultRouter()
router.register('registrations', v.RegistrationViewSet)
```

This creates:

```text
/account/api/registrations/
/account/api/registrations/<id>/
```

Simple line for class:

> Router connects a ViewSet to URLs.

## 11. What Is Browsable API?

DRF Browsable API is a web page for testing API from browser.

It shows:

- JSON response
- GET button
- POST form
- PUT form
- DELETE button

Example:

```text
http://127.0.0.1:8001/account/api/registrations/
```

Simple line for class:

> Browsable API lets us test API from browser without Postman.

## 12. What Links Should We Show In Class?

List all registrations:

```text
http://127.0.0.1:8001/account/api/registrations/
```

Show one registration:

```text
http://127.0.0.1:8001/account/api/registrations/5/
```

Change the number to check another id:

```text
http://127.0.0.1:8001/account/api/registrations/2/
http://127.0.0.1:8001/account/api/registrations/3/
```

Important:

> The id is visible now. Later, we can hide or mask some data if needed. There are processes for that.

## 13. How To Explain The Whole Thing Simply

Say this:

> Previously our project only showed HTML pages. Now we added an API for Registration. This API can show, create, update, and delete registration data using JSON. DRF helped us do this with Serializer, ViewSet, and Router.

Then show:

```text
/account/customer/
```

This is HTML page.

Then show:

```text
/account/api/registrations/
```

This is API JSON data.

Then say:

> Same database, different output. One is HTML for humans, another is JSON for software.

## 14. Current Security Note

Right now password is visible in API response.

For learning basics, we kept it simple.

In real project, we should not show password.

Later improvement:

```text
password should be write-only
password should be hashed
```

Simple line for class:

> Current API is for learning. Real apps need better password security.

## 15. Homework / Student Task

Main homework:

> Convert Bill model into API like Registration.

Students should create:

```text
BillSerializer
BillViewSet
Router registration
```

Expected API URLs:

```text
GET     /account/api/bills/
POST    /account/api/bills/
GET     /account/api/bills/<id>/
PUT     /account/api/bills/<id>/
PATCH   /account/api/bills/<id>/
DELETE  /account/api/bills/<id>/
```

Bill fields:

```text
id
customer_id
bill_id
bill_code
bill_status
bill_amount
bill_picture
created_at
```

Extra homework points:

- Test image upload.
- Test foreign key customer selection.
- Test list API.
- Test detail API.
- Test update API.
- Test delete API.

Simple assignment line:

> We converted Registration together. Now you convert Bill API by following the same pattern.

## 16. Final Mental Model

Remember this chain:

```text
Model      -> database table
Serializer -> JSON converter
ViewSet    -> API logic
Router     -> API URLs
```

Full flow:

```text
Request URL
-> Router
-> ViewSet
-> Serializer
-> Model
-> PostgreSQL
-> JSON Response
```

Easy example:

```text
GET /account/api/registrations/
```

Flow:

```text
Router sends request to RegistrationViewSet.
ViewSet gets Registration data from Model.
Serializer converts Registration data to JSON.
Browser receives JSON response.
```
