# Coderr Backend - Freelance Marketplace API

Select Language: [🇬🇧 English](#-english) | [🇩🇪 Deutsch](#-deutsch)

---

## 🇬🇧 English

This is the RESTful Backend for the **Coderr** platform, a marketplace connecting business users with customers. It was developed using **Test Driven Development (TDD)** and strictly follows **DRF best practices**.

### Table of Contents
1. [Installation & Setup](#-installation--setup)
2. [Tech Stack](#-tech-stack)
3. [API Endpoints](#-api-endpoints)
4. [Permission Matrix](#-permission-matrix)
5. [Security & Status Codes](#-security--status-codes)
6. [Testing & Quality](#-testing--quality)

---


### ⚙️ Installation & Setup
1. **Clone & Navigate**:
   ```bash
   git clone <your-repository-url>
   cd coderr-backend
   ```
2. **Environment Setup**:
   ```bash
   python -m venv .venv
   # Windows: .venv\Scripts\activate | Mac/Linux: source .venv/bin/activate
   pip install -r requirements.txt
   ```
3. **Environment Variables**:
   ```bash
   cp .env.template .env
   # Generate secret key: 
   python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
   ```
4. **Database & Server**:
   ```bash
   python manage.py migrate
   python manage.py createsuperuser
   python manage.py runserver
   ```

---

### 🛠 Tech Stack

| Tool | Version | Purpose |
| :--- | :--- | :--- |
| **Django** | 6.0.4 | Core Web Framework |
| **DRF** | 3.17.1 | REST API Toolkit |
| **Pytest** | 9.0.3 | Testing Framework (TDD) |
| **Coverage** | 7.13.5 | Quality Assurance (95%+) |
| **Django Filters** | 25.2 | Advanced Query Filtering |
| **Python Dotenv** | 1.2.2 | Environment Variable Management |

---

### 🚀 API Endpoints
All endpoints (except registration/login) require: `Authorization: Token <your-token>`

#### 🔑 Authentication & Profiles

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **POST** | `/api/registration/` | Register a new user account (Business/Customer). |
| **POST** | `/api/login/` | Login and receive an authentication token. |
| **GET** | `/api/profile/{id}/` | Retrieve detailed profile information. |
| **PATCH** | `/api/profile/{id}/` | Update your own profile details. |
| **GET** | `/api/profiles/business/` | List all available business profiles. |
| **GET** | `/api/profiles/customer/` | List all available customer profiles. |

#### 💼 Offers & Services

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/offers/` | List all offers with search and filtering. |
| **POST** | `/api/offers/` | Create a new offer with 3 packages (Business only). |
| **GET** | `/api/offers/{id}/` | Retrieve detailed offer information. |
| **PATCH** | `/api/offers/{id}/` | Update an existing offer (Owner only). |
| **DELETE** | `/api/offers/{id}/` | Delete an offer (Owner only). |

#### 🛒 Orders & Reviews

| Method | Endpoint | Description |
| :--- | :--- | :--- |
| **GET** | `/api/orders/` | List all orders related to the current user. |
| **POST** | `/api/orders/` | Create a new order (Customer only). |
| **PATCH** | `/api/orders/{id}/` | Update order status (Business only). |
| **DELETE** | `/api/orders/{id}/` | Administrative deletion (Staff only). |
| **POST** | `/api/reviews/` | Leave a review for a business (Customer only). |
| **GET** | `/api/base-info/` | Get platform-wide statistics (Public). |

---

### 🔐 Permission Matrix

| Feature | Endpoint | Requirement | Logic |
| :--- | :--- | :--- | :--- |
| **Offers** | `POST /api/offers/` | **Business** | Only business users can create listings. |
| **Orders** | `POST /api/orders/` | **Customer** | Only customers can purchase services. |
| **Reviews** | `POST /api/reviews/` | **Customer** | Only customers; max 1 review per business. |
| **Editing** | `PATCH / DELETE` | **Owner** | Restricted via universal `IsOwnerOrReadOnly`. |
| **Orders** | `DELETE /api/orders/` | **Staff** | Administrative deletion only. |

---
### 🛡 Security & Status Codes
The API strictly follows the documented HTTP status code conventions:
- **201 Created**: Resource successfully generated.
- **204 No Content**: Resource successfully deleted.
- **400 Bad Request**: Invalid input data or logic error (e.g., duplicate review).
- **401 Unauthorized**: Authentication token missing or invalid.
- **403 Forbidden**: User lacks permission for the specific resource.
- **404 Not Found**: Target resource does not exist.

---

### 🧪 Testing & Quality
- **Run all tests**: `pytest --import-mode=importlib`
- **Run with coverage**: `pytest --import-mode=importlib --cov=.`

---

## 🇩🇪 Deutsch

REST-Backend für die **Coderr**-Plattform. Marktplatz für Freelancer und Kunden. Entwickelt nach dem **TDD-Prinzip**.

### Inhaltsverzeichnis
1. [Installation & Setup](#-installation--setup)
2. [Tech-Stack](#-tech-stack)
3. [Sicherheit & Status-Codes](#-sicherheit--status-codes)
4. [Qualitätssicherung](#-qualitätssicherung)

---

### 🚀 Installation & Setup
1. **Repository klonen**:
   ```bash
   git clone <deine-repo-url>
   cd coderr-backend
   ```
2. **Umgebung einrichten**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate # Windows
   pip install -r requirements.txt
   ```
3. **Datenbank & Server**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

---

### 🛠 Tech-Stack

| Tool | Version | Zweck |
| :--- | :--- | :--- |
| **Django** | 6.0.4 | Web Framework |
| **DRF** | 3.17.1 | REST API Toolkit |
| **Pytest** | 9.0.3 | Testing (TDD) |
| **Coverage** | 7.13.5 | Qualitätssicherung |

---

### 🛡 Sicherheit & Status-Codes
Die API folgt strikt den HTTP-Statuscode-Konventionen:
- **201 Created**: Ressource erfolgreich erstellt.
- **204 No Content**: Ressource erfolgreich gelöscht.
- **400 Bad Request**: Ungültige Daten oder Logikfehler.
- **401 Unauthorized**: Token fehlt oder ist ungültig.
- **403 Forbidden**: Fehlende Berechtigung.
- **404 Not Found**: Ressource existiert nicht.

---

### 🧪 Qualitätssicherung
- **Tests**: `pytest --import-mode=importlib`
- **Abdeckung**: `pytest --import-mode=importlib --cov=.`

---
*Note: Sensitive files like `db.sqlite3` and `.env` are excluded from version control to ensure security.*
