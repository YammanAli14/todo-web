# Quick Start Guide - Phase II Todo Application

## Prerequisites

- Python 3.10+ (tested with 3.14)
- Node.js 18+ and npm
- PostgreSQL database (Neon Serverless already configured) OR SQLite for local dev

## 1. Backend Setup (5 minutes)

### Step 1: Navigate to backend directory
```bash
cd backend
```

### Step 2: Create Python virtual environment
```bash
# Windows
python -m venv venv
venv\Scripts\activate

# Mac/Linux
python3 -m venv venv
source venv/bin/activate
```

### Step 3: Install dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Configure environment
The `.env` file is already configured with Neon PostgreSQL connection. If you want to use local SQLite for development:

```bash
# Option A: Use PostgreSQL (Neon - already configured)
# DATABASE_URL is already set in .env

# Option B: Use SQLite for local development
# Edit .env and change DATABASE_URL to:
# DATABASE_URL=sqlite:///./data/todo_dev.db
```

**Current .env configuration:**
```
DATABASE_URL=postgresql://neondb_owner:npg_...@ep-lucky-voice-...aws.neon.tech/phase2
SECRET_KEY=development-secret-key-change-in-production-min-32-chars-long
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=development
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://127.0.0.1:3000
```

⚠️ **IMPORTANT:** Change `SECRET_KEY` before deploying to production!

### Step 5: Run database migrations
```bash
alembic upgrade head
```

Expected output:
```
INFO  [alembic.runtime.migration] Running upgrade  -> bab06fa45cce, Create users table
INFO  [alembic.runtime.migration] Running upgrade bab06fa45cce -> 602132887853, Create todos table
```

### Step 6: Run tests (optional but recommended)
```bash
pytest tests/ -v
```

Expected: **20 tests passing** ✅

### Step 7: Start the backend server
```bash
uvicorn src.presentation.main:app --reload --host 0.0.0.0 --port 8000
```

Backend is now running at **http://localhost:8000**

**Verify it's working:**
- Health check: http://localhost:8000/health
- API docs: http://localhost:8000/docs (FastAPI automatic Swagger UI)

---

## 2. Frontend Setup (5 minutes)

### Step 1: Open a new terminal and navigate to frontend directory
```bash
cd frontend
```

### Step 2: Install dependencies
```bash
npm install
```

This will install:
- Next.js 14
- React 18
- TypeScript 5.3
- Tailwind CSS 3
- And other dependencies

### Step 3: Configure environment
The `.env.local` file should already exist with:
```
NEXT_PUBLIC_API_URL=http://localhost:8000
NODE_ENV=development
```

If it doesn't exist, create it with the content above.

### Step 4: Start the development server
```bash
npm run dev
```

Frontend is now running at **http://localhost:3000**

---

## 3. Test the Application (2 minutes)

### Open your browser
Navigate to **http://localhost:3000**

### Test the complete flow:

1. **Landing Page**
   - Click "Get Started"

2. **Sign Up**
   - Email: `test@example.com`
   - Password: `testpassword123`
   - Click "Sign up"
   - ✅ Should auto-login and redirect to todos page

3. **Create Todos**
   - Type "Buy groceries" → Click "Add"
   - Type "Walk the dog" → Click "Add"
   - Type "Read a book" → Click "Add"
   - ✅ Should see 3 todos in the list

4. **Interact with Todos**
   - ✅ Click checkbox to mark as complete (strikethrough)
   - ✅ Click "Edit" → Change title → Click "Save"
   - ✅ Click "Delete" → Confirm → Todo removed

5. **Sign Out**
   - Click "Sign Out" button
   - ✅ Should redirect to landing page

6. **Sign In Again**
   - Click "Sign In"
   - Enter same credentials
   - ✅ Should see your todos still there!

---

## 4. Architecture Overview

```
┌─────────────────────────────────────────────────────────────┐
│                     Frontend (Next.js)                       │
│                    http://localhost:3000                     │
│                                                              │
│  - Landing Page (/)                                          │
│  - Signup (/auth/signup)                                     │
│  - Signin (/auth/signin)                                     │
│  - Todos (/todos) - Protected Route                          │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       │ REST API + JWT
                       ↓
┌─────────────────────────────────────────────────────────────┐
│                   Backend (FastAPI)                          │
│                  http://localhost:8000                       │
│                                                              │
│  Auth Endpoints:                                             │
│  - POST /auth/signup                                         │
│  - POST /auth/signin                                         │
│  - POST /auth/signout                                        │
│  - GET  /auth/me                                             │
│                                                              │
│  Todo Endpoints:                                             │
│  - GET    /todos                                             │
│  - POST   /todos                                             │
│  - GET    /todos/{id}                                        │
│  - PUT    /todos/{id}                                        │
│  - PATCH  /todos/{id}/toggle                                 │
│  - DELETE /todos/{id}                                        │
└──────────────────────┬───────────────────────────────────────┘
                       │
                       │ SQL
                       ↓
┌─────────────────────────────────────────────────────────────┐
│              Database (PostgreSQL/Neon)                      │
│                                                              │
│  Tables:                                                     │
│  - users (id, email, password_hash, created_at, updated_at)  │
│  - todos (id, user_id, title, is_complete, created_at...)    │
└─────────────────────────────────────────────────────────────┘
```

---

## 5. API Documentation

Once the backend is running, visit:
**http://localhost:8000/docs**

This is the automatic Swagger UI provided by FastAPI. You can:
- See all available endpoints
- Test endpoints directly from the browser
- View request/response schemas
- See authentication requirements

---

## 6. Troubleshooting

### Backend Issues

**Port already in use:**
```bash
# Change port in command
uvicorn src.presentation.main:app --reload --port 8001
```

**Database connection error:**
```bash
# Check DATABASE_URL in .env
# For local development, switch to SQLite:
DATABASE_URL=sqlite:///./data/todo_dev.db

# Then re-run migrations
alembic upgrade head
```

**Import errors:**
```bash
# Make sure you're in the virtual environment
# Windows: venv\Scripts\activate
# Mac/Linux: source venv/bin/activate

# Reinstall dependencies
pip install -r requirements.txt
```

### Frontend Issues

**Port 3000 already in use:**
```bash
# Next.js will automatically suggest 3001
# Or specify port:
npm run dev -- -p 3001
```

**API connection error:**
```bash
# Check .env.local
# Make sure NEXT_PUBLIC_API_URL=http://localhost:8000
# Restart dev server after changing .env.local
```

**Module not found:**
```bash
# Delete node_modules and reinstall
rm -rf node_modules package-lock.json
npm install
```

---

## 7. Running in Production

### Backend (FastAPI)

```bash
# Use gunicorn with uvicorn workers
pip install gunicorn

gunicorn src.presentation.main:app \
  --workers 4 \
  --worker-class uvicorn.workers.UvicornWorker \
  --bind 0.0.0.0:8000
```

### Frontend (Next.js)

```bash
# Build for production
npm run build

# Start production server
npm start
```

Or deploy to Vercel (recommended for Next.js):
```bash
# Install Vercel CLI
npm i -g vercel

# Deploy
vercel
```

---

## 8. Environment Variables Checklist

### Backend (.env)
- ✅ `DATABASE_URL` - PostgreSQL connection string (Neon)
- ⚠️ `SECRET_KEY` - CHANGE THIS IN PRODUCTION!
- ✅ `ALGORITHM` - HS256
- ✅ `ACCESS_TOKEN_EXPIRE_MINUTES` - 30
- ✅ `CORS_ORIGINS` - Add your production frontend URL

### Frontend (.env.local)
- ✅ `NEXT_PUBLIC_API_URL` - Your backend URL
- Update to production URL when deploying

---

## 9. Key Features Working

✅ **Authentication**
- User registration with email/password
- User login with JWT tokens
- Password hashing with bcrypt
- Protected routes

✅ **Todo Management**
- Create new todos
- View all todos
- Update todo titles
- Toggle completion status
- Delete todos
- User data isolation

✅ **User Experience**
- Responsive design (mobile to desktop)
- Real-time UI updates
- Error handling and validation
- Loading states
- Clean, modern interface

---

## 10. Next Steps

1. **Explore the API:**
   - Visit http://localhost:8000/docs
   - Try the interactive API documentation

2. **Run the tests:**
   ```bash
   cd backend
   pytest tests/ -v
   ```

3. **Customize the application:**
   - Add more fields to todos (description, due date, priority)
   - Add todo categories/tags
   - Add search and filter functionality
   - Add user profile page

4. **Deploy to production:**
   - Backend: Railway, Render, or AWS
   - Frontend: Vercel or Netlify
   - Database: Already using Neon (production-ready)

---

## Support

For issues or questions:
- Check TESTING.md for detailed testing information
- Review the README files in backend/ and frontend/ directories
- Check the code documentation and comments

**You're all set! Enjoy your Phase II Todo Application! 🎉**
