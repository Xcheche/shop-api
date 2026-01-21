# 🛍️ Shop API Endpoints

The following endpoints are available in the **Shop API**, built with Django and Django REST Framework.

---

## 🌐 Web Views
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/products/<id>/` | GET | Show product details by ID (HTML view). |
| `/cart/` | GET | Display the shopping cart contents. |
| `/` | GET | Homepage listing all products. |

---

## 🔗 API Endpoints (v1)
| Endpoint | Method | Description |
|----------|--------|-------------|
| `/api/v1/products/` | GET | List all products (supports filters, search, pagination). |
| `/api/v1/products/<id>/` | GET | Retrieve a single product by ID. |
| `/api/v1/products/create/` | POST | Create a new product (validates price > 0). |
| `/api/v1/products/modify/<id>/` | PUT/PATCH/DELETE | Update,Delete an existing product by ID (updates cache,delete cache). |


---

## 🔍 Filtering & Search
- **Filter by ID** → `/api/v1/products/?id=1`  
- **Search by name/description** → `/api/v1/products/?search=car`  
- **On-sale products** → `/api/v1/products/?on_sale=true`  
- **Pagination** → `/api/v1/products/?limit=5&offset=0`

---

## 🗄️ Cache Behavior
- **Update** → Cache is refreshed when a product is updated.  
- **Delete** → Cache entry is removed when a product is deleted.  
- Cache keys follow the format: `product_data_<id>`.

---

## 🛠️ Tech Stack
- Django 5.2.6  
- Django REST Framework  
- Django Filters  
- Pillow (for image handling)  
- SQLite/Postgres (configurable)
