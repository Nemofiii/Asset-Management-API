# Asset-Management-API
*A concurrency-safe coupon/voucher management system*
<br/>
<br/>
## 📌 Overview
This project implements a backend API for managing coupons/vouchers where multiple authenticated users can claim limited assets concurrently — without data inconsistency.

The system is designed to remain correct and consistent under high concurrency, ensuring:
- coupons are never over-claimed
- race conditions are safely handled
- users see accurate claim history
- privileged operations are protected via role-based access
<br/>

## ✨ Key Features
### 1. 🔐 Authentication & Authorization
- JWT-based authentication
- Secure password hashing
- Role-Based Access Control (RBAC)
  - USER → view & claim coupons
  - ADMIN → create, update, delete coupons
 
### 2. 🎟️ Coupon Management
- Admin-only coupon creation & updates
- Soft control via status ```(ACTIVE / INACTIVE)```
- Limited availability enforced at database level

### 3. ⚡ Concurrency Safety (Core Focus)
- Multiple users can attempt to claim the same coupon simultaneously
- Row-level locking ```(SELECT … FOR UPDATE)```
- Atomic DB transactions
- Guaranteed consistency even under race conditions

### 4. 📊 User Claim History
- Relational joins across users, coupons, and claims
- Efficient SQL queries
- Clean, JSON-serializable responses
<br/>

## 🗂️ Project Structure
```
Backend/
│
├── api/
│   ├── admin_routes.py     # Admin-only endpoints
│   ├── authenticate.py     # Auth & RBAC dependencies
│   └── user_routes.py      # User-facing endpoints
│
├── core/
│   ├── database.py
│   └── security.py         # JWT logic
│
├── models/
│   ├── claim.py
│   ├── coupon.py
│   └── user.py
│
├── services/
│   ├── auth_service.py
│   └── coupon_service.py   # Concurrency-safe claim logic
│
├── main.py
└── requirements.txt
```
<br/>

## 🛠️ Tech Stack
- Python
- FastAPI
- MySQL
- SQLAlchemy
- JWT (python-jose)
- Passlib (bcrypt)
<br/>

## 📡 API Endpoints Overview
### 1. 🎟️ User Endpoints
| Method | Endpoint                     | Description                               |
| ------ | ---------------------------- | ----------------------------------------- |
| POST	 | `/register`	                | Register a new user                       |
| POST	 | `/login`	                    | Authenticate user and return JWT          | 
| GET    | `/coupons`                   | View all active coupons                   |
| POST   | `/coupons/{coupon_id}/claim` | Claim a coupon (authenticated users only) |
| GET    | `/users/me/history`          | View claim history for the logged-in user |

### 2. 👑 Admin Endpoints
| Method | Endpoint                     | Description           |
| ------ | ---------------------------- | --------------------- |
| POST   | `/admin/coupons`             | Create a new coupon   |
| PUT    | `/admin/coupons/{coupon_id}` | Update coupon details |
| DELETE | `/admin/coupons/{coupon_id}` | Delete a coupon       |


## ⚙️ Setup Instructions
### 1️⃣ Create Virtual Environment
```
python -m venv venv
venv\Scripts\activate   # MAC: source venv/bin/activate
```

### 2️⃣ Install Dependencies
```
pip install -r requirements.txt
```

### 3️⃣ Configure Database
Create a MySQL database:
```
CREATE DATABASE assetdb;
```

Update ```DATABASE_URL```:
```
mysql+pymysql://<user>:<password>@localhost/assetdb
```

### 4️⃣ Run the Server
```
uvicorn Backend.main:app --reload
```

Server runs at:
```
http://127.0.0.1:8000
```

### 5️⃣ API Documentation (Swagger)
```
http://127.0.0.1:8000/docs
```
Use this to:
- register users
- login
- copy JWT tokens
- test endpoints
<br/>

## 🔐 Authentication Flow
1. Register
2. Login
3. Receive JWT token
4. Send token in headers:
```
token: <JWT_TOKEN>
```
<br/>

## 👑 Admin Setup
To test admin features:
```
UPDATE users SET role = 'ADMIN' WHERE email = 'admin@gmail.com';
```
Login again to receive an ADMIN token.
<br/>
<br/>
## ⚡ Concurrency Testing
This project explicitly tests race conditions.
### 1. Test Setup
Create a coupon with limited availability

### 2. Concurrency Test Command
```
TOKEN="<JWT_TOKEN>"

for i in {1..10}; do
  curl -X POST http://127.0.0.1:8000/coupons/<coupon_id>/claim \
  -H "token: $TOKEN" &
done
wait
```

### 3. Expected Result
| Outcome           | Count |
| ----------------- | ----- |
| Successful claims | 3     |
| Failed (no stock) | 7     |
| Internal errors   | 0     |

### - Concurrency Test Terminal Output:

<img width="1354" height="479" alt="image" src="https://github.com/user-attachments/assets/4d69f0e4-8037-4508-b55f-64f5e4346bb4" />

_(The image displays parallel requests attempting to claim the same coupon. With only 3 coupons available, exactly 3 concurrent requests succeeded while the remaining 7 returned 'No coupons available')_

### 4. Result
Database should now contain available count = 0, i.e 0 coupons left

### - Database Verification:

<img width="346" height="95" alt="image" src="https://github.com/user-attachments/assets/91f52c2f-1af4-4750-b9ae-9ba08abff1cc" />

_(Database verification showing the coupon’s available count reduced to zero after concurrent claim attempts)_
<br/>
<br/>
## 👥 Multi-User Concurrency Testing
To validate that the system remains consistent when multiple authenticated users attempt to claim the same coupon simultaneously, concurrency was tested using different JWT tokens, each representing a distinct user.
### 1. Test Setup
- Coupon availability: 3
- Number of concurrent users created: 5

### 2. Test command used
```
TOKENS=(
  "JWT_USER_1"
  "JWT_USER_2"
  "JWT_USER_3"
  "JWT_USER_4"
  "JWT_USER_5"
)

for TOKEN in "${TOKENS[@]}"; do
  curl -X POST http://127.0.0.1:8000/coupons/3/claim \
  -H "token: $TOKEN" &
done
wait
```

### - Concurrency Test Terminal Output:
<img width="1605" height="611" alt="image" src="https://github.com/user-attachments/assets/a5e6a76e-5dda-42f2-8bd3-fadad385a6bd" />

_(Parallel requests from multiple authenticated users attempting to claim the same coupon. With only 3 coupons available, exactly 3 requests succeeded while the remaining requests correctly returned “No coupons available.”)_
<br />
<br />
## 🧪 Error Handling Strategy
- ```404``` → Coupon not found
- ```409``` → No coupons available / concurrent update
- ```401``` → Invalid or expired token
- ```403``` → Admin access required