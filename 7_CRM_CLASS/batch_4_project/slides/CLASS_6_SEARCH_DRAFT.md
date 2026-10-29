# Class 6 review draft: Search API and filters in our Django CRM

**Theory for today's class. This Markdown is the source for the Class 6 slides. No search code has been added.**

## 1. What exists in this project

`Registration` has `id`, `name`, `email`, and `date_of_birth`. `Bill` has `customer_id`, `bill_id`, `bill_status`, `bill_amount`, and `created_at`, among other fields. These real fields give us enough material for a useful search lesson.

`/account/api/registrations/` is a JWT-protected DRF list API. It returns registrations but has **no search or filter configuration**. `/account/customer/` is an HTML customer list with a 60-second cache. Its “Search customer...” input is only visual. The router has **no Bill API** today.

All names, emails, IDs, and amounts below are illustrative sample values, not claims about current database rows. URLs containing query parameters show **planned behavior**; those searches and filters do not work yet.

## 2. Why teach a search API in this CRM?

Imagine this CRM has 50,000 registrations. A user wants **Rahim Ahmed**. Without server-side search, the Registration API returns the full list, and the client must download or page through many customers before it can find Rahim. The current `?search=rahim` parameter is ignored, and the HTML customer search box does nothing. The problem becomes visible even in this small teaching project.

A search API lets the server find the relevant rows before sending JSON to a browser or another client. The user gets a smaller, useful result, and the API has one documented rule for all clients. A small HTML-only site could also filter inside its Django view; we use an API here because this class is already learning DRF and JSON clients.

Our goal is a **basic production-style search API**: useful server-side results, clear request rules, safe fields, predictable pages, and tests. We can build these basics on `Registration` now and let students explore more advanced search later.

## 3. What is a search API, and how is it used?

A search API lets a client send a search term and receive matching records as JSON. The existing Registration list URL can accept a query parameter after `?`:

```text
GET /account/api/registrations/?search=rahim
```

The path selects the Registration collection. `search=rahim` gives the search term. After implementation, the API could return only customers whose allowed fields match “rahim”. **Right now the ViewSet ignores that parameter and returns the normal list.** The caller still needs a valid JWT token.

One possible client flow is: a user types into the customer search box → the browser sends `GET /account/api/registrations/?search=rahim` with its JWT → the ViewSet filters the queryset → the serializer returns matching customers as JSON → the browser displays the names. We must connect the existing visual box to this flow during implementation; it is not connected today.

If we add pagination and safe output, a **proposed** response could look like this. It is not the current response:

```json
{
  "count": 1,
  "next": null,
  "previous": null,
  "results": [
    {"id": 1, "name": "Rahim Ahmed", "email": "rahim@example.com", "date_of_birth": "1996-04-12"}
  ]
}
```

“Search API” names a behavior, not a new HTTP method. We normally use `GET` because searching reads records. A separate `/api/search/` endpoint might make sense for searching several resources together, but this class can use the existing Registration list endpoint.

## 4. What makes our first version credible?

The code lesson should implement a **small set of production-grade basics**, not a search engine. We can verify each item against this CRM:

1. **Server-side matching:** the API returns only customers matching the submitted term; an unknown term returns an empty list.
2. **Allowed fields and access:** search only intended fields such as `name` and `email`; require the same JWT permission as the list API.
3. **Clear filters and errors:** use exact email matching and validated dates. A bad date should produce an understandable error.
4. **Predictable results:** apply a stable order and pagination so large results can be read page by page.
5. **Safe output:** do not expose or search passwords or bill codes. The current Registration serializer exposes the password field, so that must be corrected before calling the endpoint production-ready.
6. **Checks with real requests:** test a match, no match, invalid input, and a request without a token. Measure slow queries before choosing an index.

This is enough to show students how a real product search endpoint is designed. Typo tolerance and large search engines can be later extensions.

## 5. Search, filters, and ordering

| Idea | Question | CRM example |
|---|---|---|
| Text search | Which records match these words? | Customer name contains `rah`. |
| Field filter | Which records satisfy this rule? | Bill status equals `no`. |
| Ordering | In what order should matches appear? | Newest bills first. |

The server can apply search and filters together. Ordering arranges the matches. Pagination returns a manageable part of a long list. These are related API features, but they answer different questions.

## 6. Types of text search for customers

DRF's built-in `SearchFilter` can read `?search=` once the ViewSet and searchable fields are configured. For `Registration`, the useful text fields are `name` and `email`. Its default match is case-insensitive **contains**. We can configure starts-with or exact matching too. `SearchFilter` does not automatically correct typos or rank exact matches above partial matches.

| Type | Sample input | Illustrative result | Explanation |
|---|---|---|---|
| Contains | `search=rah` | `Rahim Ahmed`, `Ayesha Rahman` | The letters occur within both names. |
| Starts with | `search=rah` on `name` | `Rahim Ahmed` | This name begins with the letters. |
| Exact email | `email=rahim@example.com` | One matching customer | An email identifies a specific account; partial email matches may be misleading. |

These are choices for the API design, not one setting that gives every behavior at once. We can allow a general partial-name search and a separate exact-email filter. The parameter names and exact rules need to be agreed before coding.

**Class check:** If we use a case-insensitive name search, `RAH` should still find `Rahim Ahmed`. An email typed with one wrong character should not silently select a different customer.

## 7. Types of field filters

These examples are **proposed URL designs**, not working endpoints. The Registration route exists; the Bill route is a future classroom example because Bill has no API yet.

| Filter | Proposed request | Intended result |
|---|---|---|
| Exact email | `/account/api/registrations/?email=rahim@example.com` | The customer with that email. |
| Exact date | `/account/api/registrations/?date_of_birth=1996-04-12` | Customers born on that date. |
| Date range | `/account/api/registrations/?born_from=1990-01-01&born_to=1999-12-31` | Customers born within both dates. |
| Bill status | `/account/api/bills/?status=no` | Bills with stored `bill_status` of `no`. Future Bill API. |
| Amount range | `/account/api/bills/?min_amount=500&max_amount=2000` | Bills from 500 through 2,000, if bounds are inclusive. Future Bill API. |
| Related customer | `/account/api/bills/?customer_id=5` | Bills linked to Registration ID 5. Future Bill API. |

`bill_status` is currently a plain text field. The code uses `yes` and `no`; it is not a formal set of model choices. We should explain filters with values the project actually stores.

## 8. Combining conditions

The `&` joins query parameters in one URL. We can define them as **AND conditions**: a record must pass each requested rule.

```text
GET /account/api/registrations/?search=rah&born_from=1990-01-01&born_to=1999-12-31
```

Imagine `Rahim Ahmed` was born in 1996, `Rahat Islam` in 2000, and `Ayesha Rahman` in 1999. The text search for `rah` may first find all three names. The date range removes Rahat. The final result contains Rahim and Ayesha.

Inside a general text search, we may check **name OR email**. The resulting matches are then combined with the date filter using **AND**. This is a useful distinction for students: “match either text field” and “also pass the date rule” can both be true.

## 9. What should the API do in edge cases?

- **No matches:** return an empty list with a normal success response. The UI can show “No customers found.”
- **Invalid date or amount:** return a clear validation error; do not quietly ignore the filter.
- **Blank search:** decide whether it shows all permitted records or none, and keep the rule consistent.
- **Many matches:** use stable ordering and pagination.
- **Sensitive fields:** never search passwords or bill codes. The current Registration serializer exposes the password field; that separate issue needs correction before production use.

The HTML page currently caches one unfiltered list under `customer_list`. When its search input is connected later, different searches must receive the correct results. The Registration API does not automatically use that HTML-page cache.

## 10. DRF tools to introduce by name

- **`SearchFilter`** is built into DRF. It can handle general text search such as `?search=rahim` after configuration.
- **`get_queryset()`** can read query parameters and apply custom Django queryset filters. It suits a small set of project-specific rules.
- **`DjangoFilterBackend`** handles structured field filters, but comes from the separate `django-filter` package. That package is **not** in this project's `requirements.txt` today.
- **`OrderingFilter`** controls result order. It supports search results but is not itself a search algorithm.

A new URL is not needed for every filter. The list endpoint can accept more than one query parameter.

## 11. Suggested class flow

1. Show the problem: the current list returns all registrations and `?search=rahim` is ignored.
2. Show how a client would send a search request and use the returned JSON.
3. Define the basic production-grade target: allowed fields, JWT, validation, stable pages, safe output, and tests.
4. Compare partial-name search with exact-email filtering.
5. Explain exact, date-range, amount-range, status, and customer filters using the real models. Label all Bill API URLs as future examples.
6. Combine search and a date filter; ask students to predict which sample customers remain.
7. Discuss no matches, invalid input, pagination, and the existing cache.

**A later class can cover** trigram typo search and custom relevance ranking. BM25, semantic, and hybrid search require richer searchable text than the current models provide.

## Teacher references

- [DRF filtering and SearchFilter](https://www.django-rest-framework.org/api-guide/filtering/)
- [DRF query parameters](https://www.django-rest-framework.org/api-guide/requests/)

**For future corrections, edit this Markdown first, then update the slide deck from it.**
