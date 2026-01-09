# Vercel Deployment Guide

This guide provides step-by-step instructions for deploying the **Phase II: Full-stack Todo Application** to Vercel.

## Project Overview

- **Backend**: FastAPI REST API (Python 3.11+) with Neon PostgreSQL
- **Frontend**: Next.js 14 with React & TypeScript
- **Architecture**: Clean architecture with domain-driven design
- **Database**: Neon Serverless PostgreSQL (cloud-hosted)

## 🚨 Important Deployment Considerations

**Vercel Limitation**: Vercel is primarily designed for frontend applications and doesn't natively support Python backends. This project requires a separate hosting solution for the backend API.

## Deployment Strategy

### Option 1: Backend + Frontend Separation (Recommended)

Deploy backend and frontend to separate platforms:

**Backend → Railway/Render/Heroku**
- Host FastAPI backend on Python-capable platform
- Keep Neon PostgreSQL database (already configured)

**Frontend → Vercel**
- Deploy Next.js frontend to Vercel
- Configure environment variables to point to backend URL

### Option 2: Backend → Vercel Serverless Functions (Limited)

Convert FastAPI endpoints to Vercel serverless functions (requires significant refactoring).

## Step-by-Step Deployment Guide

### Step 1: Prepare Environment Variables

#### Backend Environment (for Railway/Render/Heroku)

Create `.env.production` or set environment variables:

```bash
DATABASE_URL=postgresql://neondb_owner:npg_ph8e4HAmXFzR@ep-lucky-voice-ahrp7jo1-pooler.c-3.us-east-1.aws.neon.tech/phase2
SECRET_KEY=your-super-secret-key-here-min-32-characters
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
ENVIRONMENT=production
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=https://your-frontend-url.vercel.app
```

**⚠️ Security Notes:**
- Generate a new SECRET_KEY (min 32 characters)
- Update CORS_ORIGINS to include your Vercel frontend URL
- Never commit `.env` files to version control

#### Frontend Environment (for Vercel)

Set these environment variables in Vercel project settings:

```bash
NEXT_PUBLIC_API_URL=https://your-backend-url.railway.app
NODE_ENV=production
```

### Step 2: Deploy Backend (Railway Example)

#### 2.1 Create Railway Account
1. Go to [railway.app](https://railway.app)
2. Sign up with GitHub
3. Connect your GitHub repository

#### 2.2 Deploy Backend
1. In Railway dashboard, click "Deploy from GitHub Repo"
2. Select this repository
3. Choose the `backend` directory
4. Set environment variables (from Step 1)
5. Click "Deploy"

#### 2.3 Configure Database
Database is already configured in `.env` pointing to Neon PostgreSQL.

#### 2.4 Run Migrations
After deployment, run database migrations:

```bash
# SSH into Railway instance or use Railway CLI
cd backend
alembic upgrade head
```

#### 2.5 Verify Backend
Test that your backend is working:
```bash
curl https://your-backend-url.railway.app/health
# Should return: {"status":"healthy"}
```

### Step 3: Deploy Frontend to Vercel

#### 3.1 Create Vercel Account
1. Go to [vercel.com](https://vercel.com)
2. Sign up with GitHub
3. Import your GitHub repository

#### 3.2 Configure Project
1. In Vercel dashboard, click "New Project"
2. Import from GitHub
3. Select this repository
4. Configure build settings:

```
Root Directory: frontend
Build Command: npm run build
Output Directory: .next
Install Command: npm install
Development Command: npm run dev
```

#### 3.3 Set Environment Variables
In Vercel project settings → Environment Variables:

```
NEXT_PUBLIC_API_URL: https://your-backend-url.railway.app
NODE_ENV: production
```

#### 3.4 Deploy
1. Click "Deploy"
2. Wait for build completion
3. Note your production URL (e.g., `https://booseai.vercel.app`)

### Step 4: Update CORS Configuration

Update CORS_ORIGINS in your backend environment to include the Vercel frontend URL:

```bash
CORS_ORIGINS=https://booseai.vercel.app,https://your-custom-domain.com
```

### Step 5: Test the Complete Application

1. Visit your Vercel frontend URL
2. Try signing up for a new account
3. Verify that todos can be created, updated, and deleted
4. Check that authentication works properly

## Alternative Backend Hosting Options

### Render.com
1. Sign up at [render.com](https://render.com)
2. Create Web Service
3. Connect GitHub repository
4. Set environment variables
5. Deploy

### Heroku (Legacy but still works)
1. Install Heroku CLI
2. Create app: `heroku create your-app-name`
3. Set config vars: `heroku config:set KEY=value`
4. Deploy: `git push heroku main`

## File Structure for Deployment

### Backend Deployment Files
```
backend/
├── src/                    # Source code
├── requirements.txt        # Python dependencies
├── alembic.ini            # Database migrations
├── run.py                 # WSGI entry point (create this)
└── .env                   # Environment variables (local only)
```

### Frontend Deployment Files
```
frontend/
├── app/                   # Next.js app router
├── components/            # React components
├── lib/                   # Utilities
├── package.json           # Dependencies
├── next.config.js         # Next.js config
├── tsconfig.json          # TypeScript config
└── vercel.json           # Vercel config (optional)
```

## Required Deployment Files

### Create Backend Entry Point (`backend/run.py`)
```python
from src.presentation.main import app

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
```

### Optional Vercel Configuration (`frontend/vercel.json`)
```json
{
  "version": 2,
  "env": {
    "NODE_ENV": "production"
  },
  "build": {
    "env": {
      "NODE_ENV": "production"
    }
  }
}
```

## Monitoring and Maintenance

### Backend Monitoring
- Set up health checks on your hosting platform
- Monitor database connection health
- Check CORS configuration regularly

### Frontend Monitoring
- Vercel provides built-in monitoring and analytics
- Set up custom error tracking if needed

### Database Monitoring
- Neon PostgreSQL provides connection monitoring
- Monitor query performance and connection limits

## Troubleshooting

### Common Issues

1. **CORS Errors**
   - Check CORS_ORIGINS includes your frontend URL
   - Verify environment variables are set correctly

2. **Database Connection Issues**
   - Verify DATABASE_URL is correct
   - Check Neon PostgreSQL connection limits

3. **Authentication Failures**
   - Ensure SECRET_KEY is consistent between deployments
   - Verify JWT token expiration settings

4. **Build Failures**
   - Check Node.js and Python versions match development
   - Verify all dependencies are in requirements.txt/package.json

### Debugging Steps

1. Check Vercel build logs
2. Check backend hosting platform logs
3. Test API endpoints directly with curl or Postman
4. Verify environment variables are set correctly

## Production Checklist

- [ ] Generate secure SECRET_KEY
- [ ] Update CORS_ORIGINS for production URLs
- [ ] Set up database backups on Neon
- [ ] Configure custom domain (if needed)
- [ ] Set up monitoring and error tracking
- [ ] Test all authentication flows
- [ ] Verify data isolation between users
- [ ] Test API rate limiting (if implemented)

## Next Steps

After successful deployment:

1. **Set up custom domain** on Vercel
2. **Configure SSL certificates** (automatic on Vercel)
3. **Set up monitoring** with tools like Sentry or LogRocket
4. **Implement caching** for better performance
5. **Add analytics** to track user behavior

## Support

- [Vercel Documentation](https://vercel.com/docs)
- [Railway Documentation](https://docs.railway.app)
- [FastAPI Documentation](https://fastapi.tiangolo.com)
- [Next.js Documentation](https://nextjs.org/docs)