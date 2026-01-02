# Frontend - Phase II Todo Web App

Next.js frontend for the Evolution of Todo Phase II project.

## Setup

### 1. Install Dependencies

```bash
npm install
```

### 2. Configure Environment

```bash
cp .env.local.example .env.local
# Edit .env.local with your backend API URL
```

### 3. Run Development Server

```bash
npm run dev
```

The app will be available at http://localhost:3000

## Development

### Run Linter

```bash
npm run lint
```

### Run Tests

```bash
npm test
```

### Build for Production

```bash
npm run build
npm start
```

## Project Structure

```
frontend/
├── app/                    # Next.js App Router
│   ├── auth/              # Authentication pages
│   ├── todos/             # Todo management pages
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/             # React components
├── lib/                    # Utilities
│   ├── api/               # API client
│   └── types.ts           # TypeScript types
└── tests/                  # Tests
```

## Features

- User registration and authentication
- Todo list management
- Responsive design (mobile to desktop)
- Real-time validation
- Error handling
