# 🛠 Remote Inventory Management System
**An asynchronous backend service for tracking and managing hardware assets.**

This project is a high-performance REST API designed to handle inventory operations with an emphasis on speed and modern Python standards.

## 🚀 Technical Highlights
* **Asynchronous Operations:** Built using `async` and `await` for non-blocking execution.
* **Modern Database Layer:** Implements **SQLAlchemy 2.0** with an asynchronous engine.
* **Data Validation:** Uses **Pydantic V2** for strict type hinting and automatic validation.
* **Auto-Generated Docs:** Features interactive **Swagger UI** for API testing.

## 🛠 Tech Stack
* **Language:** Python 3.10+
* **Framework:** FastAPI
* **ORM:** SQLAlchemy (Async)
* **Database:** PostgreSQL

## 📁 Project Structure
```text
├── main.py          # Application entry point & routes
├── models.py        # SQLAlchemy database models
├── schemas.py       # Pydantic data validation schemas
├── database.py      # Async database connection logic
└── .gitignore       # Ignored files
