# IssuePilot

> **Production-grade Jira-like Issue Tracker** with Django REST Framework + React + PostgreSQL

A comprehensive issue tracking system featuring custom workflows, real-time notifications, full-text search, and enterprise-grade architecture.

## ✨ Features

### Core Features
- **Multi-Project Management** - Organize work across multiple projects with team access control
- **Custom Workflows** - Define states and transitions per project
- **Kanban Boards** - Visual drag-and-drop issue management
- **Agile Support** - Sprints, epics, story points, and backlog management
- **Issue Types** - Tasks, bugs, stories, and custom types
- **Advanced Search** - PostgreSQL full-text search with filters
- **Comments & Attachments** - Rich collaboration features
- **Watchers & Mentions** - Stay updated on relevant issues
- **Activity Feed** - Track all project and issue changes

### Technical Features
- **JWT Authentication** - Secure token-based auth with refresh
- **Role-Based Access** - Project owners, admins, members, viewers
- **Event-Driven Notifications** - Outbox pattern for reliable delivery
- **Celery Background Jobs** - Async notification processing
- **OpenAPI Documentation** - Auto-generated API docs with Swagger UI
- **Docker Support** - Full containerization for easy deployment
- **Production Ready** - Comprehensive error handling, logging, pagination

## 🚀 Quick Start (Docker - Recommended)

### Prerequisites
- Docker & Docker Compose
- Git

### 1. Clone and Setup

```bash
git clone <repository-url>
cd IssuePilot
cp backend/.env.example backend/.env
cp frontend/.env.example frontend/.env
```

### 2. Start All Services

```bash
docker compose up --build
```

This will start:
- **Backend** (Django + Gunicorn) → http://localhost:8000
- **Frontend** (React + Vite) → http://localhost:5173
- **PostgreSQL** → localhost:5432
- **Redis** → localhost:6379
- **Celery Worker** - Background task processing
- **Celery Beat** - Scheduled task execution

### 3. Initialize Database

In a new terminal:

```bash
# Run migrations
docker compose exec backend python manage.py migrate

# Create superuser
docker compose exec backend python manage.py createsuperuser

# Load demo data (optional)
docker compose exec backend python manage.py seed_data
```

### 4. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:8000/api/v1/
- **API Documentation**: http://localhost:8000/api/docs/
- **Django Admin**: http://localhost:8000/admin/

**Demo Credentials** (if you ran seed_data):
- Admin: `admin` / `admin123`
- Users: `alice` / `alice123`, `bob` / `bob123`, `charlie` / `charlie123`

## 🛠️ Local Development (Without Docker)

### Backend Setup

#### Prerequisites
- Python 3.11+
- PostgreSQL 15+
- Redis 7+

#### 1. Create Virtual Environment

```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

#### 2. Install Dependencies

```bash
pip install -r requirements/dev.txt
```

#### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your database credentials
```

#### 4. Setup Database

```bash
# Create database
createdb issuepilot

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Load demo data
python manage.py seed_data
```

#### 5. Run Backend

```bash
# Development server
python manage.py runserver

# In separate terminals:
# Celery worker
celery -A config worker -l info

# Celery beat
celery -A config beat -l info
```

### Frontend Setup

#### Prerequisites
- Node.js 20+
- npm or yarn

#### 1. Install Dependencies

```bash
cd frontend
npm install
```

#### 2. Configure Environment

```bash
cp .env.example .env
# Defaults should work for local development
```

#### 3. Run Frontend

```bash
npm run dev
```

Frontend will be available at http://localhost:5173

## 📁 Project Structure

```
IssuePilot/
├── backend/
│   ├── config/              # Django settings
│   │   ├── settings/        # Split settings (base, dev, prod, test)
│   │   ├── urls.py          # Main URL config
│   │   ├── celery.py        # Celery configuration
│   │   └── wsgi.py / asgi.py
│   ├── apps/
│   │   ├── users/           # User management
│   │   ├── projects/        # Projects, boards, workflows
│   │   ├── issues/          # Issues, comments, attachments
│   │   └── notifications/   # Notifications & outbox
│   ├── common/              # Shared utilities
│   │   ├── permissions.py   # Custom permissions
│   │   ├── pagination.py    # Custom pagination
│   │   ├── exceptions.py    # Error handling
│   │   └── middleware.py    # Request logging
│   ├── api/v1/              # API routing
│   ├── requirements/        # Python dependencies
│   └── manage.py
├── frontend/
│   ├── src/
│   │   ├── api/             # API client & types
│   │   ├── components/      # Reusable UI components
│   │   ├── pages/           # Page components
│   │   ├── store/           # Zustand state management
│   │   ├── lib/             # Utilities
│   │   └── main.tsx         # App entry point
│   ├── public/
│   └── package.json
├── Dockerfile.backend
├── Dockerfile.frontend
├── docker-compose.yml
└── README.md
```

## 🏗️ Architecture

### Backend Architecture

**Clean Architecture Pattern:**
- **Models** - Domain entities (Django ORM)
- **Services** - Business logic (write operations)
- **Selectors** - Query logic (read operations)
- **Serializers** - API serialization (DRF)
- **Views** - API endpoints (DRF views/viewsets)

**Key Design Patterns:**
- **Outbox Pattern** - Reliable event processing
- **Service Layer** - Business logic encapsulation
- **Repository Pattern** - Data access abstraction
- **Event Sourcing** - Activity tracking

### Frontend Architecture

**Feature-Based Structure:**
- **API Client** - Centralized axios instance with interceptors
- **TanStack Query** - Server state management & caching
- **Zustand** - Client state management (auth)
- **React Router** - Routing
- **shadcn/ui** - Accessible UI components

## 📊 Data Models

### Core Models

- **User** - Custom user model extending Django's AbstractUser
- **Project** - Container for issues with unique key
- **ProjectMembership** - User roles in projects
- **Board** - Kanban or Scrum board
- **Sprint** - Time-boxed iteration
- **Epic** - Large work item
- **Workflow** - State machine per project
- **WorkflowState** - States in workflow (To Do, In Progress, Done)
- **WorkflowTransition** - Allowed state transitions
- **Issue** - Core work item with auto-generated key (PROJ-123)
- **Comment** - Discussion on issues
- **Attachment** - File attachments
- **Watcher** - Issue followers
- **Event** - Activity tracking
- **OutboxMessage** - Transactional event processing
- **Notification** - User notifications

## 🔐 Security

- **JWT Authentication** with refresh tokens
- **CORS** configured for frontend origin
- **CSRF Protection** enabled
- **SQL Injection Prevention** via ORM
- **XSS Protection** via React
- **Input Validation** at serializer level
- **Permission Classes** for authorization
- **Environment Variables** for secrets

## 🧪 Testing

### Run Backend Tests

```bash
cd backend
python manage.py test
```

### Run Frontend Tests

```bash
cd frontend
npm test
```

## 📝 API Documentation

Interactive API documentation is available at:
- **Swagger UI**: http://localhost:8000/api/docs/
- **OpenAPI Schema**: http://localhost:8000/api/schema/

### Key Endpoints

#### Authentication
```
POST   /api/v1/auth/register/
POST   /api/v1/auth/login/
POST   /api/v1/auth/refresh/
GET    /api/v1/auth/me/
```

#### Projects
```
GET    /api/v1/projects/
POST   /api/v1/projects/
GET    /api/v1/projects/:id/
PATCH  /api/v1/projects/:id/
DELETE /api/v1/projects/:id/
GET    /api/v1/projects/:id/members/
POST   /api/v1/projects/:id/members/
GET    /api/v1/projects/:id/workflow/
```

#### Issues
```
GET    /api/v1/projects/:id/issues/
POST   /api/v1/projects/:id/issues/
GET    /api/v1/projects/:id/issues/:key/
PATCH  /api/v1/projects/:id/issues/:key/
DELETE /api/v1/projects/:id/issues/:key/
POST   /api/v1/projects/:id/issues/:key/transitions/
GET    /api/v1/projects/:id/issues/:key/comments/
POST   /api/v1/projects/:id/issues/:key/comments/
```

#### Notifications
```
GET    /api/v1/notifications/
GET    /api/v1/notifications/unread-count/
POST   /api/v1/notifications/mark-all-read/
PATCH  /api/v1/notifications/:id/
```

## 🚀 Deployment

### Environment Variables

#### Backend (.env)
```env
DJANGO_ENV=prod
SECRET_KEY=your-secret-key
DEBUG=False
ALLOWED_HOSTS=your-domain.com

POSTGRES_DB=issuepilot
POSTGRES_USER=postgres
POSTGRES_PASSWORD=your-password
POSTGRES_HOST=db
POSTGRES_PORT=5432

REDIS_URL=redis://redis:6379/0
CELERY_BROKER_URL=redis://redis:6379/1
CELERY_RESULT_BACKEND=redis://redis:6379/2

CORS_ALLOWED_ORIGINS=https://your-domain.com
```

#### Frontend (.env)
```env
VITE_API_URL=https://api.your-domain.com
```

### Production Checklist

- [ ] Set strong `SECRET_KEY`
- [ ] Set `DEBUG=False`
- [ ] Configure `ALLOWED_HOSTS`
- [ ] Set up proper database credentials
- [ ] Configure email backend (SMTP)
- [ ] Set up SSL/TLS certificates
- [ ] Configure static/media file storage (S3)
- [ ] Set up logging and monitoring
- [ ] Configure backup strategy
- [ ] Set up CI/CD pipeline

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add some amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License.

## 👥 Team

Built with ❤️ as a production-grade demonstration of modern full-stack development.

## 🙏 Acknowledgments

- Django & Django REST Framework
- React & Vite
- TailwindCSS & shadcn/ui
- PostgreSQL & Redis
- Celery
- Docker

---

**IssuePilot** - Production-grade issue tracking for modern teams.
