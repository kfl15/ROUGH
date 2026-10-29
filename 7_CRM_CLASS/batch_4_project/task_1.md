# Task 1: Smart Billing with OCR

## Project target

Upload a bill image. Read it with OCR. Fill the Billing form from the result, save the bill, and find it again by its bill ID.

Use this CRM project as an example. Apply the **API, JWT, search, and filter** ideas you learned with Registration to Billing. Use one ready-made OCR tool, such as Tesseract. You do not need to train a model or use a GPU. Use only fake data.

## Steps

1. **Create the project.** Build a Django + DRF CRM like this one. Add Registration, Bill, a Billing page, and JWT login. Add mobile to Registration, and product list and printed bill date/time to Bill. (`created_at` is the time the database record was saved.)

2. **Make 20 bill images.** Each fake image must show a bill ID, customer name, mobile number, product list, total amount, and printed date/time. Use a simple, similar format for all 20 images.

3. **Build the OCR API.** Send an image to a JWT-protected API. The API uses OCR and returns JSON with the full text and the six details from the image. If OCR reads something wrongly, keep the full text so you can check it.

4. **Fill the Billing form.** The Billing page calls the OCR API with the access token. Page code reads the JSON and fills the form automatically. Use the name and mobile number to link the bill to the right customer. Let a person check and correct the form, then save the Bill through an API.

5. **Find and search bills.** Make a protected API that returns one bill by the **bill ID printed on the image**, not the database ID. For example: `GET /account/api/bills/B-1001/`. Make a Bill details page that calls this API and shows the result. Add Bill search by bill ID or customer name, filters by customer or printed date, ordering, and pages, following the API lesson.

6. **Show the flow in Postman.** Show login and the access token. Pass it in the `Authorization: Bearer <token>` header. Upload an image with `form-data`, show the OCR JSON, save a bill, and get it by bill ID. Also show search/filter requests and a `401` response without a token.

7. **Compare by hand.** For each bill, show the image, OCR text, and saved database values. Mark what matched and what did not. If something differs, give possible reasons, such as blurry text, an OCR mistake, or a typing error.

**Submit:** Code, 20 fake bill images, a Postman collection or screenshots, and a short report with your comparison results. Do not use real customer data.
