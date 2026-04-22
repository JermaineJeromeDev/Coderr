# Coderr Backend - Freelance Marketplace API

Choose Language: [English](#english-version) | [Deutsch](#deutsch-version)

---

<h2 id="english-version">🇺🇸 English</h2>

This is the RESTful Backend for the **Coderr** platform, a marketplace connecting business users with customers. It was developed using **Test Driven Development (TDD)** and strictly follows **DRF best practices**.

### 🛠 Tech Stack


| Tool | Version | Purpose |
| :--- | :--- | :--- |
| **Django** | 6.0.4 | Core Web Framework |
| **DRF** | 3.17.1 | REST API Toolkit |
| **Pytest** | 9.0.3 | Testing Framework (TDD) |
| **Coverage** | 7.13.5 | Quality Assurance (95%+) |
| **Django Filters** | 25.2 | Advanced Query Filtering |
| **Python Dotenv** | 1.2.2 | Environment Variable Management |

### 🔐 Permission Matrix


| Feature | Endpoint | Requirement | Logic |
| :--- | :--- | :--- | :--- |
| **Offers** | `POST /api/offers/` | **Business** | Only business users can create listings. |
| **Orders** | `POST /api/orders/` | **Customer** | Only customers can purchase services. |
| **Reviews** | `POST /api/reviews/` | **Customer** | Only customers; max 1 review per business. |
| **Editing** | `PATCH / DELETE` | **Owner** | Restricted via universal `IsOwnerOrReadOnly`. |
| **Orders** | `DELETE /api/orders/` | **Staff** | Administrative deletion only. |

### 🚀 Installation
1. **Clone & Environment**:
   ```bash
   git clone <your-repo-url>
   cd coderr-backend
   cp .env.template .env # Fill in your SECRET_KEY
   ```
2. **Dependencies**:
   ```bash
   python -m venv .venv
   source .venv/bin/activate # Windows: .venv\Scripts\activate
   pip install -r requirements.txt
   ```
3. **Database**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### 🧪 Testing & Quality
We use `pytest` with a specific import mode for the modular app structure:
- **Run all tests**: `pytest --import-mode=importlib`
- **Run with coverage**: `pytest --import-mode=importlib --cov=.`

---

<h2 id="deutsch-version">🇩🇪 Deutsch</h2>

Dies ist das REST-Backend für die **Coderr**-Plattform. Die Entwicklung erfolgte nach dem **TDD-Prinzip** (Test Driven Development) unter Einhaltung strenger Clean-Code-Vorgaben.

### 🛠 Tech-Stack


| Tool | Version | Zweck |
| :--- | :--- | :--- |
| **Django** | 6.0.4 | Web Framework |
| **DRF** | 3.17.1 | REST API Toolkit |
| **Pytest** | 9.0.3 | Testing Framework (TDD) |
| **Coverage** | 7.13.5 | Qualitätssicherung (95%+) |

### 🔐 Berechtigungs-Matrix


| Feature | Endpoint | Anforderung | Logik |
| :--- | :--- | :--- | :--- |
| **Angebote** | `POST /api/offers/` | **Business** | Nur Business-User können Angebote erstellen. |
| **Bestellungen** | `POST /api/orders/` | **Customer** | Nur Kunden können Services kaufen. |
| **Reviews** | `POST /api/reviews/` | **Customer** | Nur Kunden; max. 1 Review pro Business. |
| **Editieren** | `PATCH / DELETE` | **Owner** | Geschützt durch `IsOwnerOrReadOnly`. |

### 🚀 Installation
1. **Setup**:
   ```bash
   git clone <deine-repo-url>
   cd coderr-backend
   # .env erstellen und SECRET_KEY aus .env.template eintragen
   ```
2. **Umgebung**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate # Windows
   pip install -r requirements.txt
   ```
3. **Start**:
   ```bash
   python manage.py migrate
   python manage.py runserver
   ```

### 🧪 Tests & Qualität
- **Tests starten**: `pytest --import-mode=importlib`
- **Coverage-Bericht**: `pytest --import-mode=importlib --cov=.`