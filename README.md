# Employee_Management_drf
# 🧑‍💼 Employee Management System (Django REST Framework + Jinja2)

A full-stack **Employee Management System** built with **Django REST Framework (DRF)** for the backend and **Jinja2 templates** for the frontend UI.  
This project supports user registration, authentication using **JWT tokens**, employee data management, and API documentation via **Swagger UI**.

---

## 🚀 Features

### 🔐 Authentication
- User **Sign Up** and **Login** using Django’s built-in authentication.
- **JWT-based authentication** (Access + Refresh tokens).
- Secure logout and token blacklisting.

### 👥 Employee Management
- Create, Read, Update, and Delete (CRUD) employees.
- Each user has their own employee profile.
- Upload profile pictures.
- Filter, sort, and search employees by department, name, or age.
- Pagination supported for large datasets.

### 📘 API Documentation
- **Swagger UI** and **ReDoc** available for interactive API testing and documentation.

### 💻 Frontend (UI)
- Built with **Django templates (Jinja2)**.
- Responsive **Signup**, **Login**, and **Employee List** pages.
- Uses AJAX and fetch API for communication with DRF backend.

---

## 🏗️ Tech Stack

| Component | Technology Used |
|------------|-----------------|
| Backend Framework | Django REST Framework (DRF) |
| Frontend | Django Templates (Jinja2) |
| Authentication | JWT (via `rest_framework_simplejwt`) |
| API Docs | Swagger UI (`drf-yasg`), ReDoc |
| Database | SQLite / MySQL |
| Version Control | Git & GitHub |
| Language | Python 3.12 |

---

## ⚙️ Installation Guide

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/Kothiyal2004/Employee_Management_drf.git
cd Employee_Management_drf




# Swagger UI - http://127.0.0.1:8000/swagger/