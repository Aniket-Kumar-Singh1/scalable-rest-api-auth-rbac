# internship-backend-api

FastAPI + React + PostgreSQL, containerized with Docker. JWT auth with role-based access control.

**Stack:** FastAPI · SQLAlchemy · Pydantic · python-jose · bcrypt · React · Vite · PostgreSQL · Docker

---

## Running with Docker (recommended)
```bash
git clone <repository_url>
cd scalable-rest-api-auth-rbac
docker-compose up --build
```

| Service | URL |
|---|---|
| Frontend | http://localhost |
| API (Swagger) | http://localhost:8000/docs |
| Postgres | localhost:5432 |

---

## Local development

### Database

Set `DATABASE_URL` in `backend/app/core/config.py` or a `.env` file:
```
DATABASE_URL=postgresql://postgres:postgres@localhost:5432/fastapi_db
```

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload
# → http://localhost:8000
```

### Frontend
```bash
cd frontend
npm install
npm run dev
# → http://localhost:5173
```

---

## Auth & roles

New users register with the `user` role by default. To grant admin access (admins can view all tasks system-wide), update the role directly in the database:
```sql
UPDATE users SET role = 'admin' WHERE email = 'you@example.com';
```