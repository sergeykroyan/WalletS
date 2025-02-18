# User Wallet API

## 💰 Overview
User Wallet API is a **FastAPI-based** financial system where users can:
- Create multiple **accounts**.
- Perform **deposits, withdrawals, and transfers**.
- Generate **invoices** that require admin approval before transactions occur.
- View **transaction history**.
- Admins can **approve or decline invoices**.

## 🛠️ Tech Stack
- **FastAPI** - Backend framework.
- **PostgreSQL** - Database.
- **SQLAlchemy** - ORM.
- **Alembic** - Database migrations.
- **Docker & Docker Compose** - Containerization.

## 📦 Installation & Setup
### Clone the Repository
Choose one of the following methods:
#### Clone via HTTPS
```bash
git clone https://github.com/sergeykroyan/WalletS.git
cd WalletS
```

### Configure Environment Variables
Create a `.env` file and add:
```ini
APP_CONFIG__DB__URL=postgresql+asyncpg://user:pwd@localhost:5432/app
APP_CONFIG__ACCESS_TOKEN__RESET_PASSWORD_TOKEN_SECRET=
APP_CONFIG__ACCESS_TOKEN__VERIFICATION_TOKEN_SECRET=
```


### Start the Database with Docker
```bash
docker-compose up -d
```
This will start:
- **PostgreSQL** on `localhost:5455`

### Run FastAPI Application
Create a virtual environment and install dependencies:
```bash
python -m venv venv

poetry install
```

Start the FastAPI server manually:
```bash
python main.py
```
- **PostgreSQL** on `localhost:5455`

### Run Database Migrations
```bash
alembic upgrade head
```

## 🔑 Authentication
- Uses **FastAPI Users** for token-based authentication.

## 📌 API Endpoints
### **1️⃣ Auth**
- `POST /api/v1/auth/login` → Login.
- `POST /api/v1/auth/logout` → Logout.
- `POST /api/v1/auth/register` → Register a new user (Set `is_admin=True` to be an admin).


### **2️⃣ Users**
- `GET /api/v1/users/me` → Get current user info.
- `PATCH /api/v1/users/me` → Update current user.
- `GET /api/v1/users/{id}` → Get user by ID.
- `PATCH /api/v1/users/{id}` → Update user by ID.
- `DELETE /api/v1/users/{id}` → Delete user by ID.

### **3️⃣ Accounts**
- `POST /api/v1/accounts/` → Create an account.
- `GET /api/v1/accounts/me` → Get all accounts for the authenticated user.

### **4️⃣ Invoices**
- `POST /api/v1/invoices/deposit/` → Create Deposit Invoice.
- `POST /api/v1/invoices/withdraw/` → Create Withdraw Invoice.
- `POST /api/v1/invoices/transfer/internal/` → Create Internal Transfer Invoice (User only can transfer between his accounts).
- `POST /api/v1/invoices/transfer/external/` → Create External Transfer Invoice (User only can transfer to other user accounts).
- `GET /api/v1/invoices/pending/` → Get Pending Invoices (For Admin Users only).
- `PATCH /api/v1/invoices/{invoice_id}/status/` → Update Invoice Status (For Admin Users only).

### **5️⃣ Transactions**
- `GET /api/v1/transactions/` → Get all transactions (users see only their own, admins see all).
